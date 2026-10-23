# 第三方字体、词库与数据声明

UniBeijingX 的项目代码采用 Apache License 2.0。下面的字体及第三方材料保留各自许可；字体软件及其派生位图继续采用 SIL Open Font License 1.1。

## 字体来源与修改

- **Noto Sans CJK SC Regular 2.004**：© 2014–2021 Adobe (http://www.adobe.com/)，SIL Open Font License 1.1。上游：[Noto CJK](https://github.com/notofonts/noto-cjk)。本项目将其裁剪为所需字符集，转换为 Newton SFNT 位图字库，并加入多个原生字号。
- **Noto Sans Regular 2.015**：Copyright 2022 The Noto Project Authors (https://github.com/notofonts/latin-greek-cyrillic)，SIL Open Font License 1.1。用于补充拉丁字母和符号；所用原始字体文件来自 LibreOffice 随附字体资源。本项目重新栅格化这些字符并合入派生位图字库。
- 字体对外名称为 UniBeijingX；保留上游版权，不将派生字体改授 Apache 许可证。
- 楷体“中”图标由本机 STKaiti 字形生成；项目仅保存已生成的位图图标，不分发 STKaiti 字体文件。

## 词库与数据来源

- **jieba 0.42.1**：[上游](https://github.com/fxsjy/jieba)，MIT 许可；使用其词频数据。
- **pypinyin 0.55.0**：[上游](https://github.com/mozillazg/python-pinyin)，MIT 许可；用于生成汉字拼音与候选映射。
- **中国邮政地址与邮编数据**：[公开网点查询](https://iframe.chinapost.com.cn/jsp/type/institutionalsite/SiteSearchJTApi.jsp?community=ChinaPostJT)，2026-10-15 快照，覆盖大陆 31 个省级地区、363 组省市、2,867 组区县和 37,182 组地区邮编关系。该说明是来源署名，不将中国邮政数据声明为 Apache 或 MIT 授权数据。网点邮编用于辅助填写，不能代表逐门牌投递范围。

- **台湾地名与邮递区号**：[中华邮政下载专区](https://subservices.post.gov.tw/post/internet/Download/index.jsp?ID=220306) 中的「3码邮递区号与行政区中心点经纬度对应表」XML，文件生成日期 2016-08-12，2026-10-23 获取。只使用地名和三位地区前缀，不含完整逐门牌 3+3 数据；来源 URL／SHA-256 记录于源码 `source/main/ChineseRegion/geodata/supplemental.json`。
- **香港地名**：[香港选举事务处 18 区名录](https://www.elections.gov.hk/dc2023/chi/dcgc.html)。邮政地址格式参照[万国邮联香港地址指南](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/hkgEn.pdf)及香港邮政邮编说明；不提供虚构本地邮编。
- **澳门地名与地址**：[地籍资讯网堂区名录](https://cadastre.gis.gov.mo/MGSP_Cad/chn/bak/main_20160628.html)、[教育及青年发展局地理课程指引](https://www.dsedj.gov.mo/crdc/guide/data/junior/Geography_guide_2024c.pdf)、[澳门邮电标准地址格式](https://www.ctt.gov.mo/MacauPost/Contents/AddressFormat.aspx?lang=en-us)。七堂区和路氹填海区用于地址辅助，不提供虚构本地邮编。

以上地名／邮政资料为事实数据来源署名，未将其声明为 Apache 或 MIT 授权数据；原始网站及资料权利归各来源所有。2026-10-23 核对，实际投递仍应查询邮政部门。

## SIL Open Font License 1.1

```text
This Font Software is licensed under the SIL Open Font License,
Version 1.1.

This license is copied below, and is also available with a FAQ at:
http://scripts.sil.org/OFL

-----------------------------------------------------------
SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
-----------------------------------------------------------

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects, to support the font
creation efforts of academic and linguistic communities, and to
provide a free and open framework in which fonts may be shared and
improved in partnership with others.

The OFL allows the licensed fonts to be used, studied, modified and
redistributed freely as long as they are not sold by themselves. The
fonts, including any derivative works, can be bundled, embedded,
redistributed and/or sold with any software provided that any reserved
names are not used by derivative works. The fonts and derivatives,
however, cannot be released under any other type of license. The
requirement for fonts to remain under this license does not apply to
any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright
Holder(s) under this license and clearly marked as such. This may
include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the
copyright statement(s).

"Original Version" refers to the collection of Font Software
components as distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to,
deleting, or substituting -- in part or in whole -- any of the
components of the Original Version, by changing formats or by porting
the Font Software to a new environment.

"Author" refers to any designer, engineer, programmer, technical
writer or other person who contributed to the Font Software.

PERMISSION & CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining
a copy of the Font Software, to use, study, copy, merge, embed,
modify, redistribute, and sell modified and unmodified copies of the
Font Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components, in
Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled,
redistributed and/or sold with any software, provided that each copy
contains the above copyright notice and this license. These can be
included either as stand-alone text files, human-readable headers or
in the appropriate machine-readable metadata fields within text or
binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font
Name(s) unless explicit written permission is granted by the
corresponding Copyright Holder. This restriction only applies to the
primary font name as presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
Software shall not be used to promote, endorse or advertise any
Modified Version, except to acknowledge the contribution(s) of the
Copyright Holder(s) and the Author(s) or with their explicit written
permission.

5) The Font Software, modified or unmodified, in part or in whole,
must be distributed entirely under this license, and must not be
distributed under any other license. The requirement for fonts to
remain under this license does not apply to any document created using
the Font Software.

TERMINATION
This license becomes null and void if any of the above conditions are
not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
OTHER DEALINGS IN THE FONT SOFTWARE.
```

## jieba — MIT

```text
The MIT License (MIT)

Copyright (c) 2013 Sun Junyi

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## pypinyin — MIT

```text
The MIT License (MIT)

Copyright (c) 2016 mozillazg, 闲耘 <hotoo.cn@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
