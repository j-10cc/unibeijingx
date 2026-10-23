# 校验与模拟器工具

本目录保存发布校验和隔离模拟器工具。测试状态与闪存副本放在被忽略的 `.runtime/`，不进入正式介质。

在项目根目录执行：

```sh
python3 source/main/tools/build.py --check
python3 source/main/tools/package_release.py
python3 source/test/verify_release.py
python3 source/test/verify_regions.py
```

`verify_release.py` 不依赖忽略的 docs 记录或第三方 Python 模块，检查：

- ZIP 及展开目录只包含四个 PKG、手册和引用的截图，手册与图片均与 docs 中的版本一致。
- 四个正式包的长度和 SHA-256，包格式及开发日志／界面汉化依赖符号。
- 手册包含已知问题与简短许可说明；图片链接有效，ZIP 归档注释保留完整许可，没有历史工作目录或开发阶段说明。
- 两种字体的 GB2312 覆盖、8,416 个映射字符、原生字号、75,744 条位图记录，以及字库确实嵌入相应字体包。

`build.py --check` 另在两个独立临时目录中编译全部组件，并核对已接受的 1.0.0 字节。固定包信息在 `source/main/tools/release_config.json`。

## 隔离模拟器

依赖获取和目录准备见 [external README](../../external/README.md)。

```sh
source/test/emulator/build.sh
python3 source/test/emulator/run.py my-new-profile
```

`build.sh` 在 `external/.build/emulator/` 编译带独立设置与测试命令通道的 Einstein。保留的运行介质位于 `external/emulator/runtime/EinsteinDisplay52.app`；构建不会自动替换它，如需使用新构建，应先验证并将其复制到该运行路径。

`run.py` 使用新 profile 名称，为该会话复制干净闪存并使用独立偏好设置；ROM 和基线只读，日志及命令通道在 `.runtime/<profile>/`。Ctrl+C 结束。模拟器结果不等同于真机验证；发布介质本身不含这些工具、ROM、闪存或探针。

`verify_regions.py` 检查追加模块可重生成、原大陆数据哈希不变、台湾三位邮编（允许多个区共用代码）、港澳显式留空以及全部新增地名在三套资源中的覆盖。`--baseline <目录>` 可再逐条比对追加前后全部旧字形、cmap 编号及字宽。`emulator/RegionQA.newt` 是仅用于隔离模拟器的原生运行时探针，不进入四个产品包。
