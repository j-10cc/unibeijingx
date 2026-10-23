# UniBeijingX 1.0.0 最终验收报告

本轮在 dev14 基础上修复可达界面的遗漏，最终候选为 dev15-attempt35。Lite 与 Full 使用同一固定 S0 串行验收；本报告仅对下述可达矩阵作最终结论，后续新发现问题列入下一版本。

**结论：约定范围内通过，可作为 1.0.0 正式介质。** 加载首帧、可读的周字底行裁切、-10061 专项／压力触发和 8 小时长程按用户约束排除。-10061 仍为未解决已知问题，不表示已修复。

## 本轮修复

- 共享文字与原生只读缓存：文件夹编辑、归档单选项、Country 值、Calls 等自动显示中文，并在改回英文时恢复原字体。
- 混合绘制列表完整转为独立堆对象，修复普通热重装的 -48221；安装失败的原始错误码与阶段信息正确保留。
- 原生菜单改用分段字形绘制，保留原有选择回调、标记、取消及分页；按真实文字基线修复中文底部笔画截断。
- Repeat Other、日期弹窗、日期编辑和公式日期字段使用中文回退；英文 ongoing、ISO 数字及原手写体保留。
- 总览沿用原生抽取、图标、选择与几何，仅对中文段回退；文件夹标题保留原生端帽及私有图标，长标题绘制省略且不修改记录。
- Region 的字体适配由新版字体包统一处理；内部别名共享主字库，字体列表保留单一 UniBeijingX。卸载时恢复原函数、默认字体及注册表。

## 固定环境与证据

- 原始 MP2000 ROM，Newton OS 2.1 (712000)-1；隔离 Einstein；本轮未修改 ROM 或既定验收模拟器。
- 93 个受保护文件逐一 SHA-256 核验一致，包括 5.2r1 正式介质、ROM、S0 及冻结依赖。
- 字体包源代码重建可复现；74,781 项字形位图记录审计通过。字库覆盖 8,309 个映射字符；Region 1,240 个及输入法 6,763 个中文用字静态覆盖无缺失。
- 每个测试阶段保存命令、原始截图、视图／字体状态和运行器哈希。最终截图逐一人工核阅；机械断言与视觉通过分开记录。

| 项目 | Lite | Full |
| --- | --- | --- |
| 最终候选扩展阶段 | 20 | 20 |
| 原生界面状态截图 | 154 | 157 |
| 原 ROM 像素对照零差异组数 | 28 | 28 |
| 主流程／独立冷启动／Region 先装／组件支持 | 各通过 | 各通过 |
| 英文总览启用／关闭／再启用 | 两组 0 像素差异 | 两组 0 像素差异 |
| 英文地址 China→USA→China | 两组 0 像素差异 | 两组 0 像素差异 |

## 可达矩阵

| 区域 | 已覆盖状态 |
| --- | --- |
| Notes | New menu and key；Note；Checklist；Outline；body；overview title/date/folder；Text menu；Styles font/size/face menus；action menu；folder menu；filing slip；folder editor；native class76 filing radio label。状态：empty、Roman、Chinese、mixed extended Latin/symbols、whole/partial selection、reopen、overview settled、pagination、font-only、with Region、ordinary unload/reinstall、soft/cold restart、mixed Chinese/ASCII folder name |
| Names | Person；Company；Group；Worksite；All Info；field labels and values；Add/Show/action menus；address city/province/postcode picker；folder menu；routing slip and Chinese Address preview。状态：empty、Chinese/mixed、edited/reopened、overview、picker pagination、0/1/64/255/256-char address、selection callback and stored identity |
| Selectors/Quick entry | people；meetingPlace；phone；fax；email；Quick Person；Quick Place。状态：English and Chinese rows、icons and numbers、no results、selection、new entry、save/reopen |
| Dates | Agenda empty/nonempty；Day；Week；Month；Year；Meeting editor；To Do editor；Invitees/Location；Repeat native menu；Repeat Other 8 rules；embedded calendar title and weekdays；month picker；date field；time field；alarm；cleanup-date field；Show/New/action menus。状态：Chinese date、Chinese title、seven title weekdays、3/10-second settled、redraw、previous/next month/year、selection、record unchanged、close/reopen |
| Public date popups | date；date/time；interval；multi-date。状态：Chinese month title/weekdays、month menu、previous/next、select、confirm、cancel、China-USA-China while open |
| Calls | Name；phone；notes；New/Add/Show；Other phone picker；overview/action/folder。状态：empty、English、Chinese/mixed、reopen |
| Find | query；owner selection；five-source result list；three-source results；result jump；empty result。状态：English query and Chinese records、Chinese query、sources mixed、settled、reopen |
| System/Region | Extras；Prefs list；Country；Date/Time；Formats；Owner；World Clock；Formulas list；Date Calculation；Date Conversion；currency/metric formulas；Memory Info；In/Out；Assist；Calculator；keyboard；Clock four Set modes；Owner Info list；Writing Practice；Card/Setup native icon taps。状态：English captions、Chinese locale data、China-USA-China、date picker open、stored value、bounded host/native interface availability |
| Fonts and About | canonical UniBeijingX chooser；System/Fancy/Simple/Casual/Hand/Switzerland/USA；four original Roman registries；main/private alias bitmap；About。状态：7 families whole/partial、9/10/12/18 point、5 faces、9/10/12/14/16/18 alias samples、Roman glyph pixel controls、stale palette same/different-family target、all 9 About fields、open/close/reopen |
| Package compatibility | Font-Lite；Font-Full；ChineseRegion；Pinyin。状态：font-only、Region first、font first、all components、IME actual ni -> 你 commit and saved alias、one ordinary removal/reinstall、soft restart、independent cold restart、optional component removal、locale/font registry restoration |

## 地址性能

按不超过 256 字符验收，分别测 0／1／64／255／256 字符，均完成真实 All Info 菜单选择与稳定显示；计时包含固定 2 秒等待。1,440 字符性能不列为问题。

- Lite：菜单选择及稳定等待 3.8–3.89 秒。
- Full：菜单选择及稳定等待 3.8–3.9 秒。

## 视觉及兼容性结论

中文姓名、混合来源 Find、非空 Agenda、Text／Styles、联系人选择器、标题星期、归档／文件夹、地区选择器、日期浮窗、系统偏好及公式均已触达；约定范围内未发现待修复方框。原有英文控件、New、四种 Roman 正文与 About 的像素对照，以及主字库／内部别名的六字号扩展字符像素对照均通过。扩展拉丁／符号另经实际画面与字形位图审计。About 的 Version 1.0.0、Lite／Full、j10cc、j10cc.site、Powered by GPT6.1-Sol 及其余字段在初装、重开、重装和重启后验证。

单次普通移除／重装、软重启、独立冷启动、先区域后字体、输入法实际 ni→你 输入与保存回读，以及可选组件移除后的默认区域／字体恢复均通过。没有运行反复热装卸压力或 -10061 定位。

Lite 的早期 Repeat Today 测试使用失效坐标，原始截图不计通过；已按真实菜单行坐标重跑，并断言菜单关闭。该测试工具修正不计为产品缺陷。

## 未触达及排除项

Card／Setup 原生入口在固定 S0 点击后未打开额外界面，明确列为不可达，未计内容通过。真实 MessagePad、物理打印、外部网络／传真／调制解调器／串口、未安装第三方包及任意 Unicode 组合未经验收。旧笔记兼容性排除；字库不宣称全 Unicode。

## 四包介质

Font-Lite.pkg 与 Font-Full.pkg 二选一；ChineseRegion.pkg、Pinyin.pkg 按需安装。Region 与 Pinyin 直接复用冻结二进制。发行过程不重新编译已验收候选；SHA256SUMS 与 MANIFEST.json 绑定最终文件。5.2r1 旧正式目录保留，发行不含 ROM、模拟器、闪存或测试探针。

本轮结论对应此处列明的界面、状态与环境，不作“所有输入与环境永无遗漏”的保证。本轮修复结果封版为 1.0.0，后续新发现问题进入下一版本。

## 可读边界与最终证据说明

长文件夹标题等极端边界按用户要求以仍然可读为通过标准，不要求严格控件间距。保留旧几何断言失败及对应实际截图，不把它改写成原断言通过。Lite 最终扩展矩阵分两组，各自从同一 S0 建立：前五阶段与其余十五阶段，均使用冻结候选；Full 的前十九阶段与 Country／Fancy 补验也从相同 S0 串行执行。初次 Country 点选后菜单仍开放而目标区域未切换，该次操作未计通过；保留原始日志，补充原生菜单就绪门控后重验。Lite 冷启动 About 的早期截图仅截到加载背景，已补跑并逐项核阅稳定后的九字段实图。正文和别名的最终原始像素对照均在清除插入光标、等待稳定后采集，未使用图像掩码。

## 测试工具中止与补跑说明

Lite 初次主流程完成前九阶段后，被 dev9 旧总览断言中止：旧断言要求整行 CJK 字体，和本轮保留原生 Roman 标题字体的方案冲突。新断言验证原 Roman 标题、复合 Abstract、原生抽取字节码、宽度回调和对象所有权。两次冷恢复尝试因测试探针的日志函数／安装时全局未重建而中止，均未进入产品收尾测试。另有一次验收探针使用编译器保留字导致编译中止，未进入产品安装。以上原日志、截图和失败状态保留，未计通过。

Lite 的剩余总览、普通卸载／重装、实际输入法和重启流程从相同原始 S0 重新建立 ROM／New 基线后完成；前九阶段引用初次主流程的已完成证据。前九阶段使用早期同字库候选，其后变更为绘制列表独立所有权与错误保留；最终两版各自20个扩展阶段均以最终冻结候选重新执行。Full 的完整主流程从同一 S0 执行。详细出处见 MANIFEST.json 的 acceptance 中 qa_aborted_runs、product_failed_runs、expanded_state_evidence、profiles 及各记录的阶段信息。
