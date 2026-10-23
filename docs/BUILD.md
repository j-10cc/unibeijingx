# 构建与校验

所有命令从项目根目录执行。构建使用 `external/toolchain/bin/tntk` 和 `external/toolchain/platform/Newton 2.1`，只依赖 Python 标准库；不要求从头生成字库、词典或邮政数据。

```sh
python3 source/test/verify_release.py
python3 source/main/tools/build.py --check
python3 source/main/tools/build.py
```

校验覆盖原发布 ZIP、全部 SHA256SUMS、四包清单、58 个产品源文件、311 张最终验收截图、GB2312 覆盖、8,309 个映射字符及 Lite／Full 的 74,781 条位图记录。构建在独立临时目录中完成，共享模块按工程要求复制到字体编译目录。`--check` 各编译两遍并与正式包比较，不写发布目录。普通构建写入 `release/build/`。

编译器自动写入的包头时间戳会归一为各自 1.0.0 正式文件的原时间戳。源文件与已冻结 SFNT、词典、邮政数据均随 Git 保存；移动目录后四个包仍可逐字节重现。原验收报告中的历史路径保留原文，当前路径见 `docs/source-migration.json`。

## 工具链

```sh
source/main/tools/build_toolchain.sh
```

脚本使用 `external/toolchain` 的固定版本 tntk、NEWT0 和补丁，在 `external/.build/toolchain` 中编译，将工具放回 `external/toolchain/bin/tntk`。NEWT0 已应用 UTF-8 修复，tntk 的 auto 包补丁在构建副本中应用。所有工具源码和固定提交见 `external/DEPENDENCIES.json`。需要 macOS、Apple Command Line Tools 和 CMake；这些属于宿主工具。

## 可选资源生成

常规发布构建使用已冻结资源。从轮廓字体重新栅格化会受 Pillow／FreeType 版本影响，不保证与冻结 SFNT 逐字节相同；这不影响使用冻结 SFNT 的四包精确重建。资源生成会修改源码内的数据，属于下一版本开发操作，应在开发分支进行；修改后不能再宣称与 1.0.0 完全一致。

Python 依赖下载文件和安装内容集中在 `external/python/`。资源生成使用 Python 3.14（Unicode 16.0）；较旧 Python 的 Unicode 分类会遗漏新加入的字符。本机可使用：

```sh
/opt/homebrew/bin/python3.14 -m pip install --no-index --find-links external/python/downloads --target external/python/site-packages -r external/requirements.txt
export PYTHONPATH="$PWD/external/python/site-packages:$PWD/source/main/UniBeijingX/tools"
```

- `source/main/PinyinIME/tools/build_pinyin_dict.py`：由固定 jieba／pypinyin 数据生成输入法词典。
- `source/main/ChineseRegion/tools/build_china_atlas.py`：由 `external/data/china-post` 的原始快照生成省市区和邮编数据，不覆盖正式 Region.nprj。
- `source/main/UniBeijingX/tools/build_font.py`：生成基础 GB2312 字库；还需要宿主 FontForge。默认输出至 `release/build/base-GB2312.sfnt`，不替换正式字库。
- `display52_latin_extension.py`、`display52_extended_chars.py`：保留字体扩展算法及其必要基线；基线置于 `external/fonts/baselines`。
- `build_package_icons.py`：使用已保存 PNG 生成图标。原楷体字形的首次创作使用宿主 STKaiti，正常重建使用已保存图标。

## 模拟器

```sh
python3 source/test/emulator/run.py my-new-profile
```

每次使用新名称，独立复制干净闪存，日志与命令通道位于 `source/test/.runtime/<profile>/`；ROM 和基线只读。结束使用 Ctrl+C。保留的 EinsteinDisplay52.app 使用该 profile 的 FLTK 设置，不修改全局模拟器偏好。

`source/test/emulator/build.sh` 可由本地 Einstein、FLTK、GoogleTest、NEWT64 源码和隔离设置补丁构建模拟器；构建树位于 `external/.build/emulator`。本次目录整理的验证是源码重建和发布介质校验，未重新执行 GUI 全流程；既有运行验收范围见 `docs/release/1.0.0/ACCEPTANCE_zh-CN.md`。
