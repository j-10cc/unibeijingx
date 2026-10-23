# 外部依赖与获取方法

本目录只提交本 README，其他文件和子目录均被 Git 忽略。克隆项目后，按需准备依赖；正式包编译需要工具链和平台文件，资源再生成与模拟器测试有各自的可选依赖。依赖保留上游许可，不作为 Apache 2.0 项目代码重新授权，也不进入发布 ZIP。

## 目录组织

```text
toolchain/
  tntk/                 NewtonScript 编译／打包器源码
  newt0/                编译器使用的 NEWT/0 源码
  newt64/               模拟器所用 NEWT64 源码
  platform/Newton 2.1   平台定义文件
  bin/tntk              本地编译器
  pkgdump/              可选 PKG 分析工具
fonts/                  Noto 原始字体、许可、可选资源生成基线
dictionaries/           jieba／pypinyin 原始许可副本
python/
  downloads/            固定版本 Python 依赖下载包
  site-packages/        本地安装的 Python 模块
data/china-post/        邮政网点原始快照
emulator/
  source/Einstein/      模拟器源码
  deps/fltk/            FLTK 源码
  deps/googletest/      GoogleTest 源码
  runtime/             本机 Einstein.app、EinsteinDisplay52.app 及 ROM
  fixtures/            干净测试闪存基线
reference/              可选历史参考资料
.build/                 编译器、产品包、模拟器等可重新生成的构建输出
```

下列命令均从**项目根目录**执行。项目自有补丁放在 `source/main/tools/patches/` 和 `source/test/emulator/patches/`，可随 Git 获取；不依赖本目录中的未提交清单或补丁副本。

## 1. 正式包编译必需

已验证宿主为 macOS，使用 Apple Command Line Tools（Clang、Make、Git、patch）、CMake **3.31 或更高版本**、Python **3.9 或更高版本**。Python 常规构建仅使用标准库。

固定版本：

| 依赖 | 获取位置 | 固定提交／用途 |
| --- | --- | --- |
| tntk | [ekoeppen/tntk](https://github.com/ekoeppen/tntk) | `f9f3f5dd2444997f1febd5648f60ec71a3a08afd`；MIT |
| NEWT/0 | [ekoeppen/NEWT0](https://github.com/ekoeppen/NEWT0) | `025bc268742c493fb1ce2dcea10ebeb4846652cf`；许可见其 `COPYING/` |
| Newton 2.1 平台定义 | 固定 tntk 的 `examples/native/Newton 2.1`，也可参考 [UNNA 平台文件存档](https://www.unna.org/view.php?/apple/development/NTK/platformfiles) | 由工具链脚本复制到 `toolchain/platform/` |

```sh
mkdir -p external/toolchain
git clone https://github.com/ekoeppen/tntk.git external/toolchain/tntk
git -C external/toolchain/tntk checkout f9f3f5dd2444997f1febd5648f60ec71a3a08afd
git clone https://github.com/ekoeppen/NEWT0.git external/toolchain/newt0
git -C external/toolchain/newt0 checkout 025bc268742c493fb1ce2dcea10ebeb4846652cf
source/main/tools/build_toolchain.sh
python3 source/main/tools/build.py --check
```

构建脚本在 `.build/toolchain/` 创建副本，应用 tntk auto 包和 NEWT/0 UTF-8 补丁；若本机 NEWT/0 已有同一修复，会跳过重复应用。产物是 `toolchain/bin/tntk` 和平台文件。编译正式四包使用源码中已保存的 SFNT、词典及地址数据，不需要下载原始字体或邮政快照。

## 2. 可选：重新生成字库、词典或图标

需要 Python **3.14**、Unicode **16.0** 数据库，以及下列资源工具环境。版本锁定文件随代码提交在 `source/main/tools/requirements-resources.txt`：

| Python 模块 | 版本 | 获取位置／许可 |
| --- | --- | --- |
| fonttools | 4.60.2 | [PyPI](https://pypi.org/project/fonttools/4.60.2/)；MIT 及所附第三方声明 |
| Pillow | 13.0.0 | [PyPI](https://pypi.org/project/Pillow/13.0.0/)；HPND 及所附依赖许可 |
| pypinyin | 0.55.0 | [PyPI](https://pypi.org/project/pypinyin/0.55.0/)；MIT |
| jieba | 0.42.1 | [PyPI](https://pypi.org/project/jieba/0.42.1/)；MIT |

```sh
python3.14 -m pip download --dest external/python/downloads -r source/main/tools/requirements-resources.txt
python3.14 -m pip install --no-index --find-links external/python/downloads --target external/python/site-packages -r source/main/tools/requirements-resources.txt
export PYTHONPATH="$PWD/external/python/site-packages:$PWD/source/main/UniBeijingX/tools"
```

基础字库生成还需 [FontForge](https://fontforge.org/)（其公开发行包或宿主包管理器）。本机资源验证使用 Pillow 13.0.0 所附 FreeType 2.14.3；不同栅格器版本可能产生不同位图，不能用重新生成的结果直接代替 1.0.0 已接受字库。

原始字体放在 `fonts/`，同时保留上游 OFL 文件与版权声明：

- **Noto Sans CJK SC Regular 2.004**：从 [Sans2.004 官方发行](https://github.com/notofonts/noto-cjk/releases/tag/Sans2.004) 获取 Simplified Chinese Regular OTF，命名为 `NotoSansCJKsc-Regular.otf`。本机源文件 SHA-256 为 `2c76254f6fc379fddfce0a7e84fb5385bb135d3e399294f6eeb6680d0365b74b`。
- **Noto Sans Regular 2.015**：上游 [Noto 字体存档](https://github.com/notofonts/noto-fonts/tree/main/hinted/ttf/NotoSans)及[当前字体工程](https://github.com/notofonts/latin-greek-cyrillic)。本机原文件来自 LibreOffice 随附字体，命名为 `NotoSans-Regular.ttf`，SHA-256 为 `f5f552c8c5edb61fe6efb824baf4d4de47b1a8689ab4925ff43f7bd6a4ebece5`。从上游获取的其他版本应作为新的输入重新验证。
- `fonts/baselines/dev9/`、`dev10/` 是本项目字形生成阶段保存的中间 SFNT，并非上游字体发行物；可从已有本地副本或备份恢复。它们仅供保留的扩展生成工具使用，丢失时不影响正式包编译。
- 图标生成通常读取已提交的 PNG；首次创作所用 STKaiti 属于宿主字体，不随本目录或发布包分发。

完整字体和词库许可见[第三方声明](../THIRD_PARTY_NOTICES.md)。

## 3. 可选：邮政原始数据

从[中国邮政公开网点查询](https://iframe.chinapost.com.cn/jsp/type/institutionalsite/SiteSearchJTApi.jsp?community=ChinaPostJT)获取。现有生成器使用 2026-10-15 的 54,622 条网点快照，文件名为：

```text
data/china-post/chinapost-sites-2026-10-15.json.gz
```

当时接口为 `https://iframe.chinapost.com.cn/api/institutionalsite/findlist.do`，请求参数为 `act=list&page=1&size=60000&community=ChinaPostJT`。当前接口返回的数据可能变化；要重现该快照需保留本机文件或备份，不把当前数据冒充旧快照。源码已保存全部正式地址索引和邮编二进制，日常编译无需调用该接口。

## 4. 可选：模拟器构建与测试

| 依赖 | 来源与固定版本 | 本地目录 |
| --- | --- | --- |
| Einstein | [pguyot/Einstein](https://github.com/pguyot/Einstein)，`ce9b25b9caa1affae3979aad84a6b129e7fa85aa`；GPL-2.0 | `emulator/source/Einstein` |
| FLTK | [fltk/fltk](https://github.com/fltk/fltk)，`9c70ea95a176933ffd575022d145c284d1fc9ef7`（1.4.4） | `emulator/deps/fltk` |
| GoogleTest | [v1.15.2](https://github.com/google/googletest/releases/tag/v1.15.2)；BSD-3-Clause | `emulator/deps/googletest` |
| NEWT64 | [MatthiasWM/NEWT64](https://github.com/MatthiasWM/NEWT64)，`0f1af40a847e2e6d5a620e9f9cfcd65cf45491b6` | `toolchain/newt64` |

从表中仓库克隆到指定目录，checkout 对应提交或标签，再执行：

```sh
source/test/emulator/build.sh
```

脚本先在构建副本中补齐笔触／打印命令支持，再应用隔离偏好设置补丁，不修改原始依赖。编译结果在 `.build/emulator/build/Einstein.app`。用于启动的已验证副本放在 `emulator/runtime/EinsteinDisplay52.app`；替换前应验证相应测试命令与设置隔离行为。上游自身及 FLTK 附带库的许可保留在各源码树中。

Newton ROM 需由使用者按其已有授权自行提供，放在 `emulator/runtime/mp2000-rom/mp2000.rom`；项目不提供下载。完成设备初始化后，可把没有产品包的干净闪存备份为 `emulator/fixtures/clean-final.flash`。ROM 与闪存均不提交或分发。

可选包分析工具来自 [Newton-PKGDUMP](https://github.com/RobertSundling/Newton-PKGDUMP)，固定提交 `20198e25a9c9ca4adddf4f4f8edff80e14b527cf`；克隆到 `toolchain/pkgdump/` 后按其 Makefile 编译。`reference/` 中的 UniTaipeiX、原输入法和词典归档仅作本地历史参考，可从原持有介质或 UNNA 相关软件存档恢复，不参与本版构建。
