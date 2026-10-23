# UniBeijingX

UniBeijingX 为 Apple MessagePad 2000／2100、Newton OS 2.1 提供简体中文显示、拼音输入及中文区域支持。项目目标是让 Newton 能够阅读、输入并保存中文，同时保留原生应用的操作方式和英文界面。

**当前版本：1.0.0。** [下载发布包](release/UniBeijingX-1.0.0.zip) · [用户使用手册](docs/USER_GUIDE_zh-CN.md)

## 当前能力

- **中文显示**：8,309 个映射字符，包括 GB2312、部分扩展拉丁字母及符号；为 Notes、Names、Dates、原生列表和常见选择器中的中文内容提供自动字体适配。
- **两种字体配置**：Lite 内置 9／12／16 位图字号，Full 内置 9／10／12／14／16／18；字符范围相同，安装时二选一。
- **拼音输入**：全拼候选栏、汉字与常用词、候选翻页、数字键及空格选词，配合 Newton 原生字母键盘使用。
- **中文区域**：中文日期时间、月份星期、人民币、公制、A4，以及省市区县／邮编填写辅助；通过 Prefs 的 Country 启用。
- **独立组件**：一个字体包加按需安装的输入法和区域包；不修改 ROM。字体包包含 About 页面。

本版在隔离模拟器中完成验证，真实 MessagePad 和实物打印仍待验证。字库不覆盖全部 Unicode；连续反复热装卸存在尚未解决的 `-10061` 风险，触发场景和规避方法见使用手册。

## 目录与开发入口

| 目录 | 内容与说明 |
| --- | --- |
| [source](source/README.md) | 源码组织、构建与发布流程 |
| [source/main](source/main/README.md) | 三个组件及共享构建入口 |
| [UniBeijingX](source/main/UniBeijingX/README.md) | 字体、中文内容显示适配、About |
| [PinyinIME](source/main/PinyinIME/README.md) | 输入法、词典与候选栏 |
| [ChineseRegion](source/main/ChineseRegion/README.md) | 中文区域、日期解析和邮政地址辅助 |
| [source/test](source/test/README.md) | 发布校验、字库检查与隔离模拟器工具 |
| [external](external/README.md) | 外部依赖、固定版本、获取方法及目录组织 |
| docs | 仅[用户使用手册](docs/USER_GUIDE_zh-CN.md)进入 Git；其他本地记录忽略 |
| release | 1.0.0 安装目录及 ZIP，每份介质只含四个 PKG 和使用手册 |

准备依赖后，在项目根目录执行：

```sh
python3 source/main/tools/build.py --check
python3 source/main/tools/package_release.py
python3 source/test/verify_release.py
```

普通构建输出到被忽略的 `external/.build/packages/`。外部依赖实体不进入 Git，`external` 仅提交 README。

## 许可与署名

Copyright 2026 j10cc · [j10cc.site](https://j10cc.site)。项目代码采用 [Apache License 2.0](LICENSE)。

派生位图字库基于 [Noto Sans CJK SC](https://github.com/notofonts/noto-cjk) 和 [Noto Sans](https://github.com/notofonts/latin-greek-cyrillic)，保留 **SIL Open Font License 1.1**。词库生成使用的 [jieba](https://github.com/fxsjy/jieba) 和 [pypinyin](https://github.com/mozillazg/python-pinyin) 保留 **MIT** 许可。完整版权、许可文本和数据来源见 [第三方声明](THIRD_PARTY_NOTICES.md)，同样收录于发布包的使用手册附录。
