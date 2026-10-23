# UniBeijingX 字体与显示支持

本组件生成互斥的 Font-Lite.pkg 和 Font-Full.pkg。两版均有 8,309 个映射字符；Lite 内置 9／12／16 位图字号，Full 内置 9／10／12／14／16／18。

## 代码组织与架构

- `font-lite/`、`font-full/`：各自的 `Font.nprj`、`Font.newt`、`About.newt`、`Icon.newt` 和 `UniBeijingX.sfnt`。
- `Font.newt`：安装与卸载入口、字体注册、字体族与回退判定、安装失败时的状态清理。位图数据留在包内。
- `shared/ContentDisplay.newt`：中文内容和混合文字的绘制／字体适配，覆盖受支持的列表、菜单、日期、摘要及文件夹等路径，并保留英文原生度量与回调。
- `shared/ContentFont.newt`：显示适配生命周期、视图／字体观察、延迟刷新、变更记录与卸载恢复。
- `shared/AboutView.newt`：About 表单和字体署名，与自动安装部件共同打包。
- `icons/`：已保存的位图图标源；`tools/`：字库、图标生成工具及 SFNT 解析函数。

安装时注册 `beijing`，由运行时显示适配处理中文及受支持的扩展字符。变更记录与回调令牌用于限定状态归属，并在卸载时恢复。代码不修改 ROM 文件。

## 编译

在项目根目录准备好[工具链](../../../external/README.md)后执行：

```sh
python3 source/main/tools/build.py
python3 source/main/tools/build.py --check
```

输出位于 `external/.build/packages/Font-Lite.pkg` 和 `Font-Full.pkg`。统一脚本把 `shared/*.newt` 复制到各自临时工程再编译，避免在源目录留下构建产物。`--check` 核对四个正式包，其中包括这两个字体包。

## 资源生成

常规编译直接使用本目录的 SFNT 和图标。重新生成资源时，需要 Python 3.14、fonttools、Pillow、Noto 原始字体；基础 SFNT 生成还需要 FontForge。获取方法见 external README。

- `tools/build_font.py` 生成基础 GB2312 位图字库，默认写入 `external/.build/base-GB2312.sfnt`。
- `tools/display52_latin_extension.py`、`display52_extended_chars.py` 保存字符扩展算法，使用 `external/fonts/baselines/` 中的中间字库作为输入。
- `tools/build_package_icons.py` 使用已保存 PNG 生成两个版本的图标。
- `tools/font_format.py` 提供 cmap、SFNT 表与位图记录解析，供资源工具和发布校验使用。

重新栅格化受 Pillow／FreeType 版本影响，可能与已接受的 SFNT 不同；生成器会修改资源，需作为新的产品变更重新验证。字体保留 SIL OFL 1.1，完整声明见[第三方许可](../../../THIRD_PARTY_NOTICES.md)。
