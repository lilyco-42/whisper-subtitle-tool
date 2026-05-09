from faster_whisper import WhisperModel

def seconds_to_srt_time(seconds):
    ms = int((seconds % 1) * 1000)
    s = int(seconds)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

audio_file = "七音阿卡莉 - ワンルームシュガーライフ.mp3"
model_size = "large-v3-turbo"

model = WhisperModel(model_size, device="cpu", compute_type="int8")
segments, info = model.transcribe(audio_file, language="ja")

with open(audio_file.rsplit(".", 1)[0] + ".srt", "w", encoding="utf-8") as f:
    for i, seg in enumerate(segments, 1):
        start = seg.start
        end = seg.end
        text = seg.text.strip()
        f.write(f"{i}\n{seconds_to_srt_time(start)} --> {seconds_to_srt_time(end)}\n{text}\n\n")
