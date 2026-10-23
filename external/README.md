# 本地外部依赖

本目录集中保存项目使用的第三方依赖，不随正式发布 ZIP 分发。

| 目录 | 内容 |
| --- | --- |
| toolchain | tntk、固定版本 NEWT0、NEWT64、pkgdump、补丁、编译器及 Newton 2.1 平台文件 |
| fonts | Noto CJK／Noto Sans 原始字体、许可及字形扩展必须的 dev9／dev10 基线 |
| dictionaries | jieba、pypinyin 许可 |
| python | 固定版本下载文件与本地 Python 依赖 |
| data/china-post | 邮政地址原始快照与来源说明 |
| emulator | Einstein、FLTK、GoogleTest 源码，原运行介质、ROM 和一份干净闪存基线 |
| patches | 本地第三方源码修改记录 |
| reference | UniTaipeiX、原输入法及词典的原始参考归档 |

固定来源与提交见 `DEPENDENCIES.json`；本地文件校验见 `FILES.sha256`。第三方源码保留各自授权文本。`FILES.sha256` 不包含自己、构建缓存、Python 字节码及宿主依赖路径；相对路径从项目根目录解析。依赖实体与生成缓存由 `.gitignore` 排除，Git 保存清单、Python 版本锁定及本说明。复制项目时应一并复制本目录；仅克隆 Git 不会包含这些本地依赖。

macOS、Apple Command Line Tools、Python、CMake 和可选 FontForge 是宿主工具，路径与版本记录在依赖清单；其系统库不作为项目文件复制。SDK、ROM 和闪存保留在本机，不进入 Git 或发布 ZIP。构建说明见 `docs/BUILD.md`。
