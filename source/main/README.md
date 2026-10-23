# 产品源码总览

| 目录 | 工程入口 | 输出 |
| --- | --- | --- |
| [UniBeijingX](UniBeijingX/README.md) | `font-lite/Font.nprj`、`font-full/Font.nprj` | Font-Lite.pkg、Font-Full.pkg |
| [PinyinIME](PinyinIME/README.md) | `Pinyin.nprj` | Pinyin.pkg |
| [ChineseRegion](ChineseRegion/README.md) | `Region.nprj` | ChineseRegion.pkg |
| tools | `build.py`、`build_toolchain.sh`、`package_release.py` | 统一编译、工具链构建及发布打包 |

字体包负责字库注册、中文内容显示及 About；输入法负责拼音组合、候选和提交；区域包负责 Locale、日期解析和地址辅助。三个包通过 Newton 原生文本与区域接口协作，各自管理安装和卸载状态。

`tools/release_config.json` 记录版本、工程位置、四个正式包的长度、SHA-256 与包头时间。工具链所需补丁放在 `tools/patches/`；外部工具与 SDK 位于被 Git 忽略的 `external/`。

在项目根目录执行 `python3 source/main/tools/build.py` 编译全部组件，输出到 `external/.build/packages/`；执行 `python3 source/main/tools/build.py --check` 验证 1.0.0 的两次独立重建。构建只需已保存的 SFNT、词典和地址资源，无需联网。完整步骤见 [source 说明](../README.md)及[外部依赖说明](../../external/README.md)。
