"""GUI 音频转字幕工具 - 基于 maliang + faster-whisper"""

import os
import sys
import threading
from pathlib import Path

import maliang
from faster_whisper import WhisperModel


# 处理 frozen 环境 (Nuitka 打包后 __file__ 不可靠)
if getattr(sys, 'frozen', False):
    _APP_DIR = Path(sys.executable).parent
else:
    _APP_DIR = Path(__file__).parent


def seconds_to_srt_time(seconds: float) -> str:
    ms = round((seconds % 1) * 1000)
    if ms >= 1000:
        ms = 0
        seconds += 1
    s = int(seconds)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


class TranscribeApp:
    def __init__(self):
        self.root = maliang.Tk(size=(720, 520), title="音频转字幕工具 - Whisper")

        self._model: WhisperModel | None = None
        self._model_name: str = ""
        self._running = False
        self._audio_files: list[str] = []

        self._build_ui()
        self._scan_audio_files()

    # ─── UI 构建 ──────────────────────────────────────────────

    def _build_ui(self):
        self._canvas = maliang.Canvas(self.root, auto_update=True)
        c = self._canvas

        # 标题
        maliang.Text(c, (20, 18), text="音频转字幕 (SRT)", fontsize=20, weight="bold")

        # ── 模型设置 ──
        maliang.Text(c, (20, 58), text="模型:", fontsize=14)
        self._c_model = maliang.ComboBox(
            c, (70, 48), text=(
                "tiny", "tiny.en", "base", "base.en",
                "small", "small.en", "medium", "medium.en",
                "large-v3-turbo", "large-v3"
            ),
            default=8,  # large-v3-turbo
            size=(180, 32),
        )

        maliang.Text(c, (270, 58), text="设备:", fontsize=14)
        self._c_device = maliang.ComboBox(
            c, (310, 48), text=("cpu", "cuda"), default=0, size=(90, 32),
        )

        maliang.Text(c, (420, 58), text="计算精度:", fontsize=14)
        self._c_compute = maliang.ComboBox(
            c, (490, 48), text=("int8", "int8_float16", "float16", "float32", "auto"),
            default=3, size=(130, 32),
        )

        maliang.Text(c, (20, 98), text="语言:", fontsize=14)
        self._c_lang = maliang.InputBox(
            c, (70, 88), size=(100, 32), placeholder="ja/zh/en/auto",
        )

        info_text = "选择音频文件并设置参数，点击'开始转录'。模型首次加载需下载(约1~4GB)。"
        maliang.Text(c, (20, 132), text=info_text, fontsize=11)

        # ── 音频文件列表 ──
        maliang.Text(c, (20, 165), text="音频文件:", fontsize=14, weight="bold")

        self._btn_refresh = maliang.Button(
            c, (620, 155), size=(80, 30), text="刷新列表",
            command=self._scan_audio_files,
        )

        self._sel_audio = maliang.ComboBox(
            c, (20, 195), text=("(未找到音频文件)",), default=0,
            size=(680, 32), align="down",
        )

        # ── 进度 ──
        self._progress_bar = maliang.ProgressBar(
            c, (20, 245), size=(680, 24),
        )

        self._label_status = maliang.Text(
            c, (20, 278), text="就绪", fontsize=12,
        )

        # ── 操作按钮 ──
        self._btn_start = maliang.Button(
            c, (20, 310), size=(140, 40), text="开始转录",
            command=self._start_transcribe,
        )

        self._btn_stop = maliang.Button(
            c, (180, 310), size=(100, 40), text="停止",
            command=self._stop_transcribe,
        )
        self._btn_stop.disable()

        # ── 输出信息 ──
        maliang.Text(c, (20, 370), text="输出信息:", fontsize=14, weight="bold")

        self._output_text = maliang.Text(
            c, (20, 398), text="", fontsize=11,
        )

    # ─── 音频扫描 ──────────────────────────────────────────────

    def _scan_audio_files(self):
        work_dir = _APP_DIR
        exts = (".mp3", ".wav", ".m4a", ".flac", ".ogg", ".wma", ".aac", ".opus")
        self._audio_files = sorted(
            str(p) for p in work_dir.iterdir()
            if p.suffix.lower() in exts
        )
        if not self._audio_files:
            self._audio_files = ["(未找到音频文件)"]
        # 更新 ComboBox 选项：销毁旧的，创建新的
        if hasattr(self, '_sel_audio'):
            self._sel_audio.destroy()
        self._sel_audio = maliang.ComboBox(
            self._canvas, (20, 195), text=tuple(self._audio_files), default=0,
            size=(680, 32), align="down",
        )
        self._sel_audio.lift()

    # ─── 转录逻辑 ──────────────────────────────────────────────

    def _combo_value(self, combo: maliang.ComboBox) -> str:
        """ComboBox.get() 返回索引, 用此方法获取实际文本值"""
        idx = combo.get()
        if idx is None or not combo.text:
            return ""
        return combo.text[idx]

    def _load_model(self) -> WhisperModel | None:
        model_name = self._combo_value(self._c_model) or "large-v3-turbo"
        device = self._combo_value(self._c_device) or "cpu"
        compute = self._combo_value(self._c_compute) or "auto"

        if self._model is None or self._model_name != model_name:
            self._set_status(f"正在加载模型 {model_name} ...", 0)
            try:
                self._model = WhisperModel(
                    model_name, device=device, compute_type=compute,
                )
                self._model_name = model_name
            except Exception as e:
                self._set_status(f"模型加载失败: {e}", 0)
                return None

        return self._model

    def _start_transcribe(self):
        if self._running:
            return

        audio_file = self._combo_value(self._sel_audio)
        if not audio_file or audio_file == "(未找到音频文件)":
            self._set_status("请先选择一个音频文件")
            return

        model = self._load_model()
        if model is None:
            return

        self._running = True
        self._btn_start.disable()
        self._btn_stop.disable(False)

        language = self._c_lang.get() or None

        threading.Thread(
            target=self._do_transcribe,
            args=(model, audio_file, language),
            daemon=True,
        ).start()

    def _do_transcribe(self, model: WhisperModel, audio_file: str, language: str | None):
        try:
            self._set_status("正在转录，请稍候...", 0)
            self._progress_bar.set(0)

            segments, info = model.transcribe(audio_file, language=language)
            seg_list = list(segments)

            total_dur = info.duration
            srt_path = str(Path(audio_file).with_suffix(".srt"))

            with open(srt_path, "w", encoding="utf-8") as f:
                for i, seg in enumerate(seg_list, 1):
                    if not self._running:
                        self._set_status("已停止", 0)
                        return

                    f.write(
                        f"{i}\n"
                        f"{seconds_to_srt_time(seg.start)} --> "
                        f"{seconds_to_srt_time(seg.end)}\n"
                        f"{seg.text.strip()}\n\n"
                    )
                    pct = min(seg.end / total_dur, 1.0) if total_dur else 0
                    self._progress_bar.set(pct)
                    self._set_status(
                        f"转录中... [{i}/{len(seg_list)}]  {seg.text.strip()[:50]}",
                        pct,
                    )

            self._set_status(f"完成! 已保存 → {srt_path}", 1.0)
            self._output_text.set(f"输出: {os.path.abspath(srt_path)}")
        except Exception as e:
            self._set_status(f"转录失败: {e}")
        finally:
            self._running = False
            self._btn_start.disable(False)
            self._btn_stop.disable()

    def _stop_transcribe(self):
        self._running = False

    def _set_status(self, msg: str, progress: float | None = None):
        self.root.after(0, lambda: self._label_status.set(msg))
        if progress is not None:
            self.root.after(0, lambda: self._progress_bar.set(progress))

    def run(self):
        self.root.center()
        self.root.mainloop()


if __name__ == "__main__":
    TranscribeApp().run()
