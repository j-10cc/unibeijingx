# Chinese Region

本组件生成 ChineseRegion.pkg，提供中文区域、日期解析及邮政地址填写辅助。首次安装注册 `zhCN:Beijing` 区域，由用户在 Prefs 的 Country 中选择中国后启用。

## 代码组织与架构

- `Region.nprj`：自动安装包工程，列出全部模块和 31 个省级数据模块。
- `Region.newt`：安装／卸载状态、Locale 注册、Country 选择与区域切换、相关显示缓存及设置恢复。
- `DateParser.newt`：中文日期与 ISO 日期解析；仅在该区域有效时适配公开日期解析路径，检查年月日有效性。
- `NamesLocalization.newt`：Names 地址／日期字段的适配与辅助行为。
- `RegionsLocalization.newt`：邮政查询选择器、地址格式、区域默认值及打印格式注册。
- `ChinaProvince0.newt` 至 `ChinaProvince30.newt`：省市区县索引；`ChinaData.newt`：数据根；`ChinaCodes.bin`：保留前导零的邮编压缩数据。
- `LocalizationUI.sfnt`：区域专用字体资源；`Icon.newt`：图标资源；`tools/build_china_atlas.py`：邮政数据生成器。

区域状态与内容字体由各自组件管理。区域包记录所管理的默认值和对象变更，切换或卸载时按状态归属恢复；系统标签保持英文，中文月份、星期、日期时间和地名属于区域内容。地址选择器在启用中国区域且地址 Country 为 China／中国时工作。

## 编译

在项目根目录准备好[工具链](../../../external/README.md)后执行：

```sh
python3 source/main/tools/build.py
python3 source/main/tools/build.py --check
```

输出为 `external/.build/packages/ChineseRegion.pkg`。常规编译直接读取本目录保存的数据和字体，不依赖原始邮政快照。也可在临时工程中以 `tntk -P <平台目录> -c Region.nprj` 单独编译。

## 数据生成

原始数据放在 `external/data/china-post/`。具备对应 2026-10-15 快照后，在项目根目录执行：

```sh
python3 source/main/ChineseRegion/tools/build_china_atlas.py
```

生成器校验 54,622 个原始网点，去重生成省市区县索引、邮编二进制和本地数据清单，不改写 Region.nprj。更新快照属于产品数据变更，应重新核验。数据为地址填写辅助，不设置时区，也不保证逐门牌投递范围。来源与字体许可见[第三方声明](../../../THIRD_PARTY_NOTICES.md)，操作说明见[使用手册](../../../docs/USER_GUIDE_zh-CN.md)。
