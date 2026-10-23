# UniBeijingX

面向 MessagePad 2000／2100、Newton OS 2.1 的简体中文支持。

当前正式版本为 **1.0.0**，正式分支为 **master**。选择 Lite／Full 字体之一，按需安装拼音输入法和中文区域包。应用界面保持英文，5.3 界面汉化保存在独立的 **feature/dev5.3** 分支。

[下载本地发布包](release/UniBeijingX-1.0.0.zip) · [安装说明](docs/release/1.0.0/README_zh-CN.md) · [验收范围与已知边界](docs/release/1.0.0/ACCEPTANCE_zh-CN.md)

```text
source/
  main/
    UniBeijingX/     Lite、Full、共享显示适配、About、字库及生成工具
    PinyinIME/       输入法、词典及生成工具
    ChineseRegion/   中文区域、日期解析、邮政地址库及生成工具
    tools/           正式包及工具链构建入口
  test/              发布校验及隔离模拟器工具
release/             已冻结正式安装包与 ZIP；临时构建输出在 build/
external/            本地第三方源码、工具、Python 依赖、字体、SDK、ROM 和测试基线
docs/                安装与验收说明、构建说明、来源及最终验收证据
```

在项目根目录执行：

```sh
python3 source/test/verify_release.py
python3 source/main/tools/build.py --check
```

第二条命令在临时目录中将四个组件各构建两次，并与 1.0.0 逐字节比较。普通构建使用 `python3 source/main/tools/build.py`，输出到 `release/build/`。

详见[构建说明](docs/BUILD.md)、[目录整理记录](docs/REPOSITORY.md)及[外部依赖说明](external/README.md)。ROM、闪存及本地第三方依赖不进入 Git 和正式 ZIP；本地依赖目录通过清单和校验值记录。真机、物理打印等未验收范围沿用 1.0.0 的声明。
