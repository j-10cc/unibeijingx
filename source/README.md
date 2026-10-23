# 源码与构建

本目录保存可进入 Git 的产品代码、资源和测试工具。项目统一使用 `source` 作为源码目录名。

```text
main/
  UniBeijingX/       Lite／Full 字体、共享显示适配、About 与字形工具
  PinyinIME/         输入法、词典及生成器
  ChineseRegion/     区域设置、日期解析、地址数据及生成器
  tools/             统一构建、发布打包、固定包信息及工具链补丁
test/
  verify_release.py  发布内容、包哈希及字库结构检查
  emulator/          隔离模拟器的构建与启动
```

三个产品均为 NewtonScript 工程，通过 tntk 和 Newton 2.1 平台文件编译。字体使用自动安装部件注册字库与显示适配，并提供一个 About 表单；输入法为带候选栏的表单包；区域设置为独立自动安装包。它们在运行时使用 Newton 对象、原生键盘和 Locale 接口，卸载时撤销自身管理的状态。

组件细节见 [main 总览](main/README.md)、[字体](main/UniBeijingX/README.md)、[输入法](main/PinyinIME/README.md)、[区域](main/ChineseRegion/README.md)。

## 编译

所有下列命令从**项目根目录**执行。先按 [external 说明](../external/README.md) 准备固定版本 tntk、NEWT0 和平台文件；常规产品构建只使用 Python 标准库与 tntk，不需要重新生成字体或词典。

```sh
source/main/tools/build_toolchain.sh
python3 source/main/tools/build.py
python3 source/main/tools/build.py --check
```

普通构建写入 `external/.build/packages/`。编译器写入的包头时间采用 `main/tools/release_config.json` 中的固定值。`--check` 在两个独立临时目录中构建各组件，与已接受的 1.0.0 哈希及发布目录中的文件逐字节比较，不覆盖正式包。

构建脚本会把字体的共享 `.newt` 文件复制到临时工程，再调用相应 `.nprj`。如需从字体轮廓、词库或邮政快照重新生成资源，按各组件 README 操作；这类操作会改变生成资源，不属于常规正式包编译。

## 准备发布介质

```sh
python3 source/main/tools/package_release.py
python3 source/test/verify_release.py
```

打包脚本核对四个已接受 PKG，复制当前用户手册，生成 `release/UniBeijingX-1.0.0.zip`。ZIP 中严格只有四个安装文件和手册；完整许可文本放在手册附录。发布内容与字库检查见 [test 说明](test/README.md)。
