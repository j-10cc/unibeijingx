# UniBeijingX

UniBeijingX 为 Apple MessagePad 2000／2100、Newton OS 2.1 提供简体中文显示、拼音输入及中文区域支持。项目目标是让 Newton 能够阅读、输入并保存中文，同时保留原生应用的操作方式和英文界面。

**当前版本：1.0.0。** [下载发布包](https://github.com/j-10cc/unibeijingx/releases/tag/v1.0.0) · [用户使用手册](docs/USER_GUIDE_zh-CN.md)

## 当前能力

- **中文显示**：8,416 个映射字符，包括 GB2312、台湾／香港／澳门地名用字、部分扩展拉丁字母及符号；为 Notes、Names、Dates、原生列表和常见选择器中的中文内容提供自动字体适配。
- **两种字体配置**：Lite 内置 9／12／16 位图字号，Full 内置 9／10／12／14／16／18；字符范围相同，安装时二选一。
- **拼音输入**：全拼候选栏、汉字与常用词、候选翻页、数字键及空格选词，配合 Newton 原生字母键盘使用。
- **中文区域**：中文日期时间、月份星期、人民币、公制、A4，以及含台湾、香港、澳门的地区／邮编填写辅助；通过 Prefs 的 Country 启用。
- **独立组件**：一个字体包加按需安装的输入法和区域包；不修改 ROM。字体包包含 About 页面。

本版在隔离模拟器中完成验证，并在 Apple Newton MessagePad 2000实机完成安装和基础功能验证。字库不覆盖全部 Unicode；连续反复热装卸存在尚未解决的 `-10061` 风险，触发场景和规避方法见使用手册。

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
| docs | [用户使用手册](docs/USER_GUIDE_zh-CN.md)及 `image/` 中的模拟器截图 |
| release | 本地发布介质，不进入 Git；正式下载通过 GitHub Releases 提供 |

准备依赖后，先从上方 GitHub Release 下载正式 ZIP 并解压到本地 `release/`，形成 `release/UniBeijingX-1.0.0/` 目录，再在项目根目录执行校验或重新打包：

```sh
python3 source/main/tools/build.py --check
python3 source/main/tools/package_release.py
python3 source/test/verify_release.py
```

普通构建输出到被忽略的 `external/.build/packages/`。外部依赖实体不进入 Git，`external` 仅提交 README。

## 许可与署名

Copyright 2026 j-10cc · [j10cc.site](https://www.j10cc.site)。项目代码采用 [Apache License 2.0](LICENSE)。第三方材料保留各自许可，派生位图字库继续采用 SIL Open Font License 1.1。

| 材料 | 来源与版权 | 本项目用途／许可 |
| --- | --- | --- |
| Noto Sans CJK SC Regular 2.004 | [Noto CJK](https://github.com/notofonts/noto-cjk)，© 2014–2021 Adobe | 裁剪字符集，转换为 Newton SFNT 多字号位图；SIL OFL 1.1 |
| Noto Sans Regular 2.015 | [The Noto Project Authors](https://github.com/notofonts/latin-greek-cyrillic)，Copyright 2022；本机原字体来自 LibreOffice 随附资源 | 补充拉丁字母与符号，并合入派生位图字库；SIL OFL 1.1 |
| jieba 0.42.1 | [jieba](https://github.com/fxsjy/jieba)，Copyright 2013 Sun Junyi | 词频与常用词数据；MIT |
| pypinyin 0.55.0 | [pypinyin](https://github.com/mozillazg/python-pinyin)，Copyright 2016 mozillazg、闲耘 | 生成拼音读音和候选映射；MIT |
| 中国邮政地名及邮编 | [中国邮政公开网点查询](https://iframe.chinapost.com.cn/jsp/type/institutionalsite/SiteSearchJTApi.jsp?community=ChinaPostJT)，2026-10-15 快照 | 辅助填写地址；覆盖大陆 31 个省级地区、363 组省市、2,867 组区县及 37,182 组地区邮编关系；不将其声明为 Apache／MIT 授权数据 |

地区选择器另补充台湾 22 县市及 371 条邮政地区记录、香港 18 区、澳门 7 堂区及路氹填海区。台湾提供三位地区前缀（非完整逐门牌六位码），港澳邮编留空；地理分组不虚构市县。来源见 [第三方声明](THIRD_PARTY_NOTICES.md)。

派生字体以 UniBeijingX 名称提供，保留上游字体版权。楷体“中”图标由本机 STKaiti 字形生成，项目仅保存已生成位图，不分发 STKaiti 字体文件。邮政网点邮编不代表逐门牌投递范围，使用时应核对实际地址。

完整第三方版权和许可正文见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)，项目许可证全文见 [LICENSE](LICENSE)。发布 ZIP 的归档注释也保存这两份文件的完整文本，可用 `unzip -z release/UniBeijingX-1.0.0.zip` 查看；用户手册保留简短的许可说明。
