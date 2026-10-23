# Pinyin IME

本组件生成 Pinyin.pkg，提供配合 Newton 原生字母键盘使用的拼音候选栏。

## 代码组织与架构

- `Pinyin.nprj`：表单包工程，加载 Main、Dictionary 和 Icon。
- `Main.newt`：安装／卸载、候选栏单窗口管理、拼音缓冲、候选显示与翻页、数字及空格选词、输入目标绑定和汉字提交；同时包含 Notes 中文 Find 的补充路径。
- `Dictionary.newt`：生成的拼音到汉字／词语候选映射，编译时直接嵌入包。
- `dictionary-manifest.json`：词典规模及生成来源，覆盖 6,763 个 GB2312 汉字和 3,006 个词语。
- `Icon.newt`：Extras 图标；`tools/build_pinyin_dict.py`：词典生成器。

候选栏保存组合状态，通过 ABC 打开原生键盘并绑定目标字段；提交时向原生文本字段写入选中的 Unicode 字符。关闭后可从 Extras 重新打开；卸载时撤销候选栏和本组件登记的回调。

## 编译

在项目根目录准备好[工具链](../../../external/README.md)后执行：

```sh
python3 source/main/tools/build.py
python3 source/main/tools/build.py --check
```

输入法输出为 `external/.build/packages/Pinyin.pkg`。常规编译使用已保存词典，不需要 Python 第三方模块。也可在临时工程中使用 `tntk -P <平台目录> -c Pinyin.nprj` 单独编译。

## 词典生成

准备 external README 所列 Python 依赖后，在项目根目录执行：

```sh
PYTHONPATH="$PWD/external/python/site-packages" python3.14 source/main/PinyinIME/tools/build_pinyin_dict.py
```

生成器读取 jieba 词频和 pypinyin 读音，写回 `Dictionary.newt` 与清单。候选范围以 GB2312 汉字为基础，词语根据频率及内置常用词选择。生成后应重新编译并验证；字典材料的 MIT 许可见[第三方声明](../../../THIRD_PARTY_NOTICES.md)。用户操作见[使用手册](../../../docs/USER_GUIDE_zh-CN.md)。
