# Maliang 库完整文档 (v3.1.5)

> **maliang** 是一个基于 `tkinter` 的轻量级 UI 框架，所有控件均由 Canvas 绘制。
> GitHub: https://github.com/Xiaokang2022/maliang
> 文档: https://xiaokang2022.github.io/maliang-docs/
> PyPI: `pip install maliang`

---

## 1. 安装

```bash
pip install maliang              # 基础安装
pip install maliang[opt]          # 包含所有可选依赖
pip install maliang[ext]          # 包含所有官方扩展包
```

### 依赖

| 类型 | 包名 |
|------|------|
| 必需 | `typing-extensions` |
| 可选增强 | `darkdetect`, `pillow`, `pywinstyles`, `hPyT`, `win32material` |
| 官方扩展 | `maliang-mpl` (matplotlib), `maliang-media` (媒体播放), `maliang-three` (3D), `maliang-table` (表格) |

---

## 2. 架构概览

```
maliang
├── core/           # 核心框架
│   ├── configs.py  # 全局配置 (Env, Font, Constant)
│   ├── containers.py # 容器 (Tk, Toplevel, Canvas)
│   └── virtual.py  # 虚拟基类 (Element, Shape, Text, Image, Style, Feature, Widget)
├── standard/       # 标准实现
│   ├── widgets.py  # 所有标准控件
│   ├── features.py # 控件交互功能
│   ├── shapes.py   # 形状元素
│   ├── texts.py    # 文本元素
│   ├── images.py   # 图像元素
│   ├── styles.py   # 样式定义
│   └── dialogs.py  # 对话框
├── animation/      # 动画系统
│   ├── animations.py  # 动画类
│   └── controllers.py # 控制函数
├── color/          # 颜色处理
│   ├── convert.py  # 颜色格式转换
│   ├── rgb.py      # RGB 运算
│   ├── hsl.py      # HSL
│   └── colortable.py # 颜色名映射表
├── theme/          # 主题管理
│   └── manager.py  # 主题切换/系统监听
└── toolbox/        # 工具
    ├── enhanced.py # 增强的 tkinter 类 (PhotoImage)
    └── utility.py  # 工具函数
```

---

## 3. 核心类 (core)

### 3.1 配置 (configs.py)

```python
import maliang

# Env - 环境配置
maliang.Env.system          # "Windows10" / "Windows11" / "Linux" / "Darwin"
maliang.Env.theme           # "light" / "dark"
maliang.Env.gradient_animation  # bool, 是否默认启用渐变动画
maliang.Env.auto_update     # bool, 是否自动检查更新
maliang.Env.root            # 当前默认根窗口 (只读)
maliang.Env.reset()         # 重置所有配置

# Font - 字体配置
maliang.Font.family         # 默认字体族 ("Microsoft YaHei"/"SF Pro"/"Noto Sans")
maliang.Font.size           # 默认字体大小 (负数表示像素, 默认 -20)
maliang.Font.reset()        # 重置字体配置

# Constant - 常量
maliang.Constant.GOLDEN_RATIO           # 黄金比例 (≈0.618)
maliang.Constant.PREDEFINED_EVENTS      # 预定义事件元组
maliang.Constant.PREDEFINED_VIRTUAL_EVENTS  # 预定义虚拟事件元组

# 重置所有配置
maliang.reset()
```

### 3.2 容器 (containers.py)

#### Tk - 主窗口

```python
root = maliang.Tk(
    size=(1280, 720),        # 窗口尺寸
    position=(100, 100),     # 窗口位置 (None=默认, 负数=从右下角算)
    title="窗口标题",
    icon="icon.ico"          # 或 maliang.PhotoImage 对象
)
```

**属性/方法:**

| 方法 | 说明 |
|------|------|
| `root.ratios` | 缩放比例 `(w_ratio, h_ratio)` |
| `root.canvases` | 所有子 Canvas 列表 |
| `root.light` / `root.dark` | 明/暗主题色字典 |
| `root.geometry(size=..., position=...)` | 设置/获取窗口大小位置 |
| `root.center(refer=None)` | 居中窗口 (refer 为参考控件) |
| `root.icon(value)` | 设置图标 |
| `root.alpha(value)` | 设置/获取透明度 (0~1) |
| `root.topmost(value)` | 设置/获取置顶 |
| `root.fullscreen(value)` | 设置/获取全屏 |
| `root.theme("light" or "dark")` | 切换主题 |
| `root.at_exit(command)` | 设置关闭时的回调 |
| `root.toolwindow(value)` | (仅 Windows) 工具窗口 |
| `root.transparentcolor(value)` | (仅 Windows) 穿透色 |
| `root.modified(value)` | (仅 macOS) 修改状态 |
| `root.transparent(value)` | (仅 macOS) 透明 |

#### Toplevel - 弹出窗口

```python
popup = maliang.Toplevel(
    master=root,
    size=(960, 540),
    title="弹出窗口",
    grab=False,     # 是否捕获所有事件
    focus=True,     # 是否获取焦点
)
# 继承 Tk 的所有方法
```

#### Canvas - 主容器

所有虚拟控件的父容器是 `Canvas`。

```python
canvas = maliang.Canvas(
    master=root,
    expand="xy",            # 扩展模式: ""/"x"/"y"/"xy"
    auto_zoom=False,        # 是否自动缩放子项
    keep_ratio=None,        # 保持比例: "min"/"max"/None
    free_anchor=False,      # 自由锚点
    auto_update=True,       # 主题管理器自动更新
    zoom_all_items=False,   # 是否缩放所有画布项
)
```

**属性/方法:**

| 方法 | 说明 |
|------|------|
| `canvas.ratios` | 缩放比例 |
| `canvas.widgets` | 所有子控件列表 |
| `canvas.canvases` | 所有嵌套 Canvas 列表 |
| `canvas.auto_update` | 是否自动更新主题 |
| `canvas.theme("light"/"dark")` | 切换主题 |
| `canvas.zoom()` | 缩放 |
| `canvas.clear()` | 清空所有内容 |
| `canvas.register_event(name)` | 注册事件 |
| `canvas.hide_focus()` | 隐藏焦点矩形 |

### 3.3 虚拟基类 (virtual.py)

Widget = Element + Style + Feature

#### Element (抽象基类)

所有可见元素的基类。

| 方法 | 说明 |
|------|------|
| `element.move(dx, dy)` | 移动 |
| `element.moveto(x, y)` | 移动到指定位置 |
| `element.destroy()` | 销毁 |
| `element.center()` | 几何中心坐标 |
| `element.region()` | 判定区域 (x1, y1, x2, y2) |
| `element.detect(x, y)` | 检测坐标是否在元素内 |
| `element.update(state)` | 更新样式到对应状态 |
| `element.configure(style)` | 配置样式并立即更新 |
| `element.forget(value=True)` | 隐藏/显示 |
| `element.zoom(ratios)` | 缩放 |

#### Shape (形状)

继承 Element。创建各种几何形状。

#### Text (文本)

继承 Element。显示和编辑文本。

| 属性 | 说明 |
|------|------|
| `text.text` | 文本内容 |
| `text.font` | 字体对象 (tkinter.font.Font) |
| `text.show` | 显示替代字符 (如密码框) |
| `text.placeholder` | 占位文本 |
| `text.limit` | 字符限制数量 |

#### Image (图像)

继承 Element。显示图片。

| 属性 | 说明 |
|------|------|
| `image.image` | 当前图像 |
| `image.initial_image` | 原始图像 |

#### Style

控件的样式系统。

| 属性 | 说明 |
|------|------|
| `style.states` | 状态元组 |
| `style.light` | 亮色主题样式数据 |
| `style.dark` | 暗色主题样式数据 |
| `style.auto_update` | 是否自动更新 |
| `style.get(theme=None)` | 获取样式数据 |
| `style.reset(theme=None)` | 重置样式 |
| `style.detach()` | 从类数据分离 (使实例数据独立) |
| `style.set()` | 设置样式 (子类重写) |

#### Feature

控件的交互功能。

| 方法 | 说明 |
|------|------|
| `feature.get_method(name)` | 按事件名获取方法 |
| `feature.extra_commands` | 额外绑定的命令字典 |

#### Widget (基类控件)

所有控件的基类。

| 属性/方法 | 说明 |
|------|------|
| `widget.master` | 父容器/控件 |
| `widget.position` | 位置 |
| `widget.size` | 尺寸 |
| `widget.state` | 当前状态字符串 |
| `widget.elements` | 所有元素 (shapes + texts + images) |
| `widget.children` | 所有子控件 |
| `widget.nested` | 是否为嵌套控件 |
| `widget.offset` | 锚点偏移量 |
| `widget.update(state)` | 更新控件状态 |
| `widget.disable(value=True)` | 禁用/启用 |
| `widget.forget(value=True)` | 隐藏/显示 |
| `widget.lift()` | 置于顶层 |
| `widget.move(dx, dy)` | 移动 |
| `widget.moveto(x, y)` | 移动到 |
| `widget.destroy()` | 销毁 |
| `widget.exists()` | 是否存在 |
| `widget.region()` | 判定区域 |
| `widget.detect(x, y)` | 检测坐标 |
| `widget.center()` | 中心坐标 |
| `widget.zoom(ratios)` | 缩放 |
| `widget.resize(size)` | 调整大小 |
| `widget.bind(sequence, command)` | 绑定事件 |
| `widget.unbind(sequence, command)` | 解绑事件 |
| `widget.bind_on_update(command)` | 绑定更新钩子 |
| `widget.generate_event(sequence, event)` | 生成事件 |

---

## 4. 标准控件 (standard/widgets.py)

### 4.1 Text - 纯文本显示

```python
text = maliang.Text(
    canvas, (100, 50),
    text="Hello World",
    family="Microsoft YaHei",
    fontsize=20,
    weight="normal",          # "normal" / "bold"
    slant="roman",            # "roman" / "italic"
    underline=False,
    overstrike=False,
    justify="left",           # "left" / "center" / "right"
    wrap_length=None,         # 自动换行宽度
)
text.get()    # 获取文本
text.set(s)  # 设置文本
```

### 4.2 Image - 静态图片

```python
img = maliang.Image(
    canvas, (100, 50),
    image=photo_image,
)
img.get()     # 获取 PhotoImage
img.set(img)  # 设置图片
```

### 4.3 Label - 标签

```python
label = maliang.Label(
    canvas, (100, 50),
    text="标签文本",
    image=photo_image,  # 可选
)
label.get()  # 获取文本
label.set(s) # 设置文本
```

### 4.4 Button - 按钮

```python
btn = maliang.Button(
    canvas, (100, 50),
    text="点击我",
    command=lambda: print("被点击了"),
    image=photo_image,  # 可选
)
btn.get()  # 获取文本
btn.set(s) # 设置文本
```

### 4.5 Switch - 开关

```python
switch = maliang.Switch(
    canvas, (100, 50),
    length=60,
    default=False,
    command=lambda v: print(f"开关状态: {v}"),
)
switch.get()           # 获取 bool 状态
switch.set(True)       # 设置状态
switch.set(True, callback=True)  # 设置并触发回调
```

### 4.6 InputBox - 单行输入框

```python
input_box = maliang.InputBox(
    canvas, (100, 50),
    size=(200, 30),
    placeholder="请输入...",
    show="*",          # 密码遮罩
    limit=50,          # 字符数限制
    limit_width=0,     # 宽度限制
    align="left",      # "left" / "center" / "right"
)
input_box.get()             # 获取文本
input_box.set("text")       # 设置文本
input_box.insert(0, "abc") # 插入
input_box.append("def")     # 追加
input_box.remove(0, 2)      # 删除 (start, end)
input_box.pop()             # 弹出末尾字符
input_box.clear()           # 清空
```

### 4.7 CheckBox - 复选框

```python
cb = maliang.CheckBox(
    canvas, (100, 50),
    length=30,
    default=False,
    command=lambda v: print(f"选中: {v}"),
)
cb.get()           # bool
cb.set(True)
```

### 4.8 RadioBox - 单选按钮

```python
rb1 = maliang.RadioBox(canvas, (100, 50), length=30, command=lambda v: print(v))
rb2 = maliang.RadioBox(canvas, (100, 90), length=30)
rb3 = maliang.RadioBox(canvas, (100, 130), length=30)

rb1.group(rb2, rb3)  # 编组 (互斥)
rb1.set(True)        # 选中
```

### 4.9 ToggleButton - 切换按钮

```python
toggle = maliang.ToggleButton(
    canvas, (100, 50),
    text="切换",
    default=False,
    command=lambda v: print(f"状态: {v}"),
)
toggle.get()  # bool
toggle.set(True)
```

### 4.10 ProgressBar - 进度条

```python
bar = maliang.ProgressBar(
    canvas, (100, 50),
    size=(400, 20),
    default=0.0,
    command=lambda v: print(f"进度: {v*100}%"),
)
bar.get()     # float (0~1)
bar.set(0.5)  # 设置进度
```

### 4.11 Slider - 滑块

```python
slider = maliang.Slider(
    canvas, (100, 50),
    size=(400, 30),
    default=0.5,
    command=lambda v: print(f"值: {v}"),
)
slider.get()    # float (0~1)
slider.set(0.8) # 设置值
```

### 4.12 SpinBox - 数值输入

```python
spin = maliang.SpinBox(
    canvas, (100, 50),
    size=(200, 30),
    format_spec="d",   # "d" / "f" / ".2f" 等
    step=1,
    default="0",
)
spin.get()      # 获取字符串值
spin.set("42")  # 设置值
spin.clear()    # 清空
```

### 4.13 ComboBox - 下拉组合框

```python
combo = maliang.ComboBox(
    canvas, (100, 50),
    text=("选项1", "选项2", "选项3"),
    default=0,
    command=lambda i: print(f"选中索引: {i}"),
    align="down",  # "up" / "down"
)
combo.get()     # int | None
combo.set(1)
```

### 4.14 OptionButton - 选项按钮

类似 ComboBox，但使用按钮触发选项菜单。

```python
opt = maliang.OptionButton(
    canvas, (100, 50),
    text=("选项A", "选项B", "选项C"),
    default=0,
    command=lambda i: print(f"选中: {i}"),
    align="center",  # "up" / "center" / "down"
)
```

### 4.15 SegmentedButton - 分段按钮

```python
seg = maliang.SegmentedButton(
    canvas, (100, 50),
    text=("日", "周", "月", "年"),
    layout="horizontal",  # "horizontal" / "vertical"
    default=0,
    command=lambda i: print(f"选中: {i}"),
)
seg.get()     # int | None
seg.set(2)
```

### 4.16 Spinner - 加载指示器

```python
spinner = maliang.Spinner(
    canvas, (100, 50),
    size=(30, 30),
    mode="determinate",   # "determinate" / "indeterminate"
    widths=(4, 3),        # (外环宽, 内环宽)
)
spinner.set(0.75)  # 仅 determinate 模式有效
spinner.get()       # float
```

### 4.17 UnderlineButton - 下划线按钮 (用于链接)

```python
link = maliang.UnderlineButton(
    canvas, (100, 50),
    text="点击访问",
    command=lambda: webbrowser.open("https://example.com"),
)
```

### 4.18 HighlightButton - 高亮按钮 (无边框)

```python
hbtn = maliang.HighlightButton(
    canvas, (100, 50),
    text="高亮按钮",
    command=lambda: print("点击"),
)
```

### 4.19 IconButton - 带图标按钮

```python
icon_btn = maliang.IconButton(
    canvas, (100, 50),
    text="带图标",
    image=icon_photo,
    command=lambda: print("点击"),
)
```

### 4.20 Tooltip - 工具提示

```python
tooltip = maliang.Tooltip(
    button,  # 关联的控件
    text="这是提示信息",
    align="down",  # "up"/"down"/"left"/"right"/"center"
    padding=3,
)
```

---

## 5. 形状 (standard/shapes.py)

| 形状类 | 说明 |
|------|------|
| `shapes.Rectangle` | 矩形 |
| `shapes.Oval` | 椭圆/圆形 |
| `shapes.Arc` | 弧形 |
| `shapes.Line` | 线段 (通过 points 参数定义关键点) |
| `shapes.RegularPolygon` | 正多边形 (参数: side 边数, angle 旋转弧度) |
| `shapes.RoundedRectangle` | 圆角矩形 (参数: radius 圆角半径) |
| `shapes.HalfRoundedRectangle` | 半圆角矩形 (参数: radius, ignore="left"/"right") |
| `shapes.SemicircularRectangle` | 半圆形两端矩形 |
| `shapes.SharpRectangle` | 尖角矩形 (参数: theta, ratio) |
| `shapes.Parallelogram` | 平行四边形 (参数: theta 倾斜弧度) |

---

## 6. 文本 (standard/texts.py)

| 文本类 | 说明 |
|------|------|
| `texts.Information` | 通用信息文本 (只读显示) |
| `texts.SingleLineText` | 单行可编辑文本 |

**Information 方法:** `get()`, `set(text)`, `append(text)`, `delete(num)`, `clear()`

**SingleLineText 额外方法:** `insert(index, text)`, `remove(start, end)`, `pop(index)`, `cursor_move(count)`, `cursor_move_to(index)`, `text_proxy` (高级操作)

---

## 7. 图像 (standard/images.py)

| 图像类 | 说明 |
|------|------|
| `images.StillImage` | 静态图像 |
| `images.Smoke` | 烟熏效果 (注释掉的, 需要 Pillow) |

---

## 8. 样式系统 (standard/styles.py)

每个控件都有对应的 Style 类，定义了在不同状态下的颜色。

**状态列表 (states):**

通用: `("normal", "hover", "active", "disabled")`
开关类: `("normal-off", "hover-off", "active-off", "normal-on", "hover-on", "active-on", "disabled")`

**Style 类的 `set()` 方法示例:**

```python
# 按钮样式
button.style.set(
    theme="light",  # None 表示两者都设置
    fg=("#1A1A1A", "#1A1A1A", "#1A1A1A"),  # normal, hover, active
    bg=("#E1E1E1", "#E5F1FB", "#CCE4F7"),
    ol=("#C0C0C0", "#288CDB", "#4884B4"),
)
# 使用 ... (Ellipsis) 跳过某个状态
button.style.set(fg=(..., "#FF0000", ...))  # 只改 hover 的前景色
```

| Style 类 | 对应控件 | 可设置参数 |
|------|------|------|
| `TextStyle` | Text | `fg` |
| `LabelStyle` | Label | `fg`, `bg`, `ol` |
| `ButtonStyle` | Button | `fg`, `bg`, `ol` |
| `SwitchStyle` | Switch | `bg_slot`, `ol_slot`, `bg_dot`, `ol_dot` |
| `InputBoxStyle` | InputBox | `fg`, `bg`, `ol`, `bg_bar` |
| `ToggleButtonStyle` | ToggleButton | `fg`, `bg`, `ol` |
| `CheckBoxStyle` | CheckBox | (继承 ToggleButtonStyle) |
| `RadioBoxStyle` | RadioBox | `bg_box`, `ol_box`, `bg_dot`, `ol_dot` |
| `ProgressBarStyle` | ProgressBar | `bg_slot`, `ol_slot`, `bg_bar`, `ol_bar` |
| `SliderStyle` | Slider | `fg_slot`, `bg_slot`, `bg_pnt`, `bg_dot` |
| `SegmentedButtonStyle` | SegmentedButton | `bg`, `ol` |
| `OptionButtonStyle` | OptionButton | `bg`, `ol` |
| `SpinnerStyle` | Spinner | `fg`, `bg` |
| `TooltipStyle` | Tooltip | `fg`, `bg`, `ol` |
| `UnderlineButtonStyle` | UnderlineButton | `fg` |
| `HighlightButtonStyle` | HighlightButton | `fg` |
| `IconButtonStyle` | IconButton | `fg`, `bg`, `ol` |

---

## 9. 动画系统 (animation/)

### Animation - 基础动画类

```python
from maliang.animation import Animation, controllers

anim = Animation(
    duration=1000,           # 持续时间 (ms)
    command=lambda p: print(p),  # 每帧回调, p ∈ [0, 1]
    controller=controllers.smooth,  # 控制函数
    end=lambda: print("完成"),  # 结束回调
    fps=60,                  # 帧率
    repeat=0,                # 重复次数 (-1=无限)
    repeat_delay=0,          # 重复延迟
    derivation=False,        # 回调是否导数
)
anim.start()
anim.stop()
```

### 内置动画类

| 类 | 说明 |
|------|------|
| `MoveWindow` | 移动窗口 |
| `MoveTkWidget` | 移动 tkinter 原生控件 |
| `MoveWidget` | 移动虚拟控件 |
| `MoveElement` | 移动元素 |
| `MoveItem` | 移动画布项 |
| `GradientTkWidget` | 渐变色控件 |
| `GradientItem` | 渐变色画布项 |
| `ScaleFontSize` | 缩放字体大小 |

### 控制器函数 (controllers)

| 函数 | 说明 |
|------|------|
| `linear` | 线性 |
| `smooth` | 平滑 (ease-in-out) |
| `rebound` | 回弹 |
| `ease_in` | 缓入 |
| `ease_out` | 缓出 |
| `generate` | 自定义生成器 |

---

## 10. 颜色系统 (color/)

### 格式转换 (convert.py)

| 函数 | 说明 |
|------|------|
| `rgb_to_hex(rgb)` | RGB → 十六进制 |
| `hex_to_rgb(hex)` | 十六进制 → RGB |
| `rgba_to_hex(rgba)` | RGBA → 十六进制 |
| `hex_to_rgba(hex)` | 十六进制 → RGBA |
| `hsl_to_rgb(hsl)` | HSL → RGB |
| `rgb_to_hsl(rgb)` | RGB → HSL |
| `name_to_rgb(name)` | 颜色名 → RGB |
| `rgb_to_name(rgb)` | RGB → 颜色名列表 |
| `str_to_rgb(str)` | 颜色名/HEX → RGB |
| `fix_hex_length(hex)` | 修复 HEX 长度 |
| `rgba_to_rgb(rgba, refer=bg)` | RGBA → RGB (混合背景) |

每种都有对应的短别名: `rgb2hex`, `hex2rgb` 等。

### RGB 运算 (rgb.py)

| 函数 | 说明 |
|------|------|
| `contrast(value, channels=...)` | 获取对比色 |
| `transition(first, second, rate)` | 颜色过渡 |
| `blend(*values, weights=None)` | 按权重混合多个颜色 |
| `gradient(first, second, count, rate, controller)` | 生成渐变色列表 |

---

## 11. 主题管理 (theme/manager.py)

```python
import maliang.theme as theme

# 颜色模式
theme.set_color_mode("system")   # "system" / "light" / "dark"
theme.get_color_mode()           # "light" / "dark"

# 事件注册
theme.register_event(func, *args)  # 系统主题切换时调用
theme.remove_event(func)

# Windows 主题效果
theme.apply_theme(window, theme="mica")  # mica/acrylic/acrylic2/aero/transparent/...

# 窗口定制
theme.customize_window(
    window,
    border_color="#FF0000",
    header_color="#333333",
    title_color="#FFFFFF",
    hide_title_bar=False,
    hide_button="maxmin",
    disable_minimize_button=False,
    disable_maximize_button=True,
    border_type="round",
)

# 文件拖放 (仅 Windows)
theme.apply_file_dnd(window, command=lambda path: print(path))
```

---

## 12. 对话框 (standard/dialogs.py)

| 对话框 | 说明 |
|------|------|
| `TkMessage` | 消息弹窗 |
| `TkColorChooser` | 颜色选择器 |
| `TkFontChooser` | 字体选择器 |

```python
# 消息弹窗
maliang.TkMessage(
    message="操作成功",
    detail="文件已保存",
    title="提示",
    icon="info",           # "error"/"info"/"question"/"warning"
    option="ok",           # "ok"/"okcancel"/"yesno"/"yesnocancel"/"retrycancel"/"abortretryignore"
    default="ok",
    command=lambda r: print(f"用户选择了: {r}"),
)

# 颜色选择器
maliang.TkColorChooser(
    title="选择颜色",
    color="#FF0000",
    command=lambda c: print(f"选择了: {c}"),
)

# 字体选择器
maliang.TkFontChooser(
    title="选择字体",
    command=lambda f: print(f"选择了: {f}"),
)
```

---

## 13. 工具箱 (toolbox/)

### PhotoImage (enhanced.py)

增强的 tkinter PhotoImage，支持缩放:

```python
img = maliang.PhotoImage(file="image.png")
scaled = img.scale(0.5, 0.5)    # 按比例缩放
resized = img.resize(100, 100)  # 按像素缩放
```

### 工具函数 (utility.py)

| 函数 | 说明 |
|------|------|
| `get_parent(widget)` | 获取 Windows HWND |
| `embed_window(window, parent)` | 嵌入窗口 |
| `load_font(font_path, private=True)` | 加载字体文件 |
| `screen_size()` | 获取屏幕尺寸 |
| `get_text_size(text, fontsize, family)` | 计算文本所需尺寸 |
| `fix_cursor(name)` | 跨平台修正光标名 |
| `create_smoke(size, color)` | 创建烟雾效果 PhotoImage |

### Trigger 类

```python
trigger = utility.Trigger(lambda: print("触发"))
trigger.update(True)  # 触发
trigger.reset()       # 重置
trigger.lock()        # 锁定
trigger.unlock()      # 解锁
```

---

## 14. 完整示例

```python
import maliang

# 创建主窗口
root = maliang.Tk(size=(800, 600), title="maliang 示例")

# 创建 Canvas
canvas = maliang.Canvas(root, auto_update=True)

# 添加控件
label = maliang.Label(canvas, (50, 30), text="用户名:")
input_box = maliang.InputBox(canvas, (150, 20), size=(200, 30), placeholder="请输入用户名")

label2 = maliang.Label(canvas, (50, 80), text="密码:")
pwd_box = maliang.InputBox(canvas, (150, 70), size=(200, 30), show="*", placeholder="请输入密码")

switch = maliang.Switch(canvas, (50, 120), length=60, default=False)

def on_login():
    username = input_box.get()
    switch_state = switch.get()
    # 登录逻辑...

btn = maliang.Button(canvas, (50, 180), text="登录", command=on_login)

# 进度条
bar = maliang.ProgressBar(canvas, (50, 230), size=(300, 20))
bar.set(0.6)

root.mainloop()
```

---

## 15. 扩展包

| 包 | 功能 | 安装 |
|------|------|------|
| `maliang-mpl` | matplotlib 集成 | `pip install maliang-mpl` |
| `maliang-media` | 媒体文件播放 (视频/音频) | `pip install maliang-media` |
| `maliang-three` | 简单 3D 绘图 | `pip install maliang-three` |
| `maliang-table` | 表格控件 | `pip install maliang-table` |
| Magic-Brush | 可视化拖拽 GUI 构建器 | 独立应用 |

---

## 16. 关键设计概念

1. **Canvas 绘制一切**: 所有控件通过 Canvas API 绘制，而非 tkinter 原生控件
2. **Widget = Element + Style + Feature**: 控件由外观元素 (Shape/Text/Image)、样式 (Style) 和交互功能 (Feature) 组成
3. **状态驱动样式**: 控件在不同状态 (normal/hover/active/disabled) 下展示不同颜色
4. **渐变色彩动画**: 状态切换时通过 `GradientItem` 实现平滑颜色过渡
5. **主题系统**: 支持明/暗主题自动切换，可跟随系统设置
6. **锚点系统**: 控件支持 9 种锚点定位 (nw/n/ne/w/center/e/sw/s/se)
7. **嵌套控件**: Widget 可以嵌套其他 Widget
8. **事件捕获**: 支持事件捕获控制，可阻止事件穿透
