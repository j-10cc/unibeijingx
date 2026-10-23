# UniBeijingX 1.0.0 使用手册

UniBeijingX 为 Apple MessagePad 2000／2100、Newton OS 2.1 提供简体中文显示、拼音输入和中文区域支持。作者：j10cc · [j10cc.site](https://j10cc.site)。

## 1. 包的功能与选择

发布包包含四个安装文件。字体选择 Lite 或 Full 其中一个，输入法与区域包按需安装。

| 文件 | 功能 | 如何选择 |
| --- | --- | --- |
| Font-Lite.pkg | 中文字体、自动中文内容显示适配、About；内置 9／12／16 位图字号 | 较小的字体包；与 Full 二选一 |
| Font-Full.pkg | 与 Lite 相同的字符集和显示功能；内置 9／10／12／14／16／18 位图字号 | 需要更多原生字号时选择；与 Lite 二选一 |
| Pinyin.pkg | 拼音候选栏，配合 Newton 原生字母键盘输入汉字和词语 | 需要中文输入时安装 |
| ChineseRegion.pkg | 中文月份、星期、日期和时间格式、人民币、公制、A4，以及中国邮政地址查询辅助 | 需要中文区域设置时安装 |

两个字体包均提供 8,309 个映射字符，包含 GB2312 字符、部分扩展拉丁字母和符号。安装字体后，Notes、Names、Dates 等受支持界面中的中文内容自动使用中文字形；英文菜单、按钮及 City／State／Zip Code 等标签保持英文。

## 2. 安装

### 安装前准备

1. 备份 Newton 中的重要数据，并准备可向设备传送 `.pkg` 文件的安装工具；也可在已配置好的 Newton 模拟器中安装。
2. 解压 `UniBeijingX-1.0.0.zip`。目录内应有四个 `.pkg` 和本手册。
3. 保存当前编辑内容，关闭 Find、日期选择器、编辑表单和输入浮窗。

### 安装顺序

1. 安装 **Font-Lite.pkg 或 Font-Full.pkg**。两者使用相同包标识，不能同时安装。
2. 需要中文区域时，安装 **ChineseRegion.pkg**。
3. 需要拼音输入时，安装 **Pinyin.pkg**。
4. 在 **Extras → UniBeijingX** 打开 About，确认显示 **Version 1.0.0**，并核对 Lite／Full。
5. 安装区域包后，在 **Extras → Prefs → Locale → Country** 选择 **中国**。安装区域包本身不会自动替用户选择国家。

只需要阅读中文时，安装一个字体包即可。要输入中文，再安装 Pinyin；要使用中文日期、人民币和地址查询，再安装 ChineseRegion。

## 3. 使用

### 中文显示和字体

安装字体包后，受支持的文本、列表和日期显示会自动适配中文，无需为每个字段手工更改字体。需要主动设置字体时，在原生字体选择器中选择 **UniBeijingX**。Lite 与 Full 的字符范围相同，区别是内置位图字号数量。

### 拼音输入

1. 在文本字段中点选输入位置；从 **Extras → Pinyin IME** 打开候选栏。
2. 点候选栏右侧 **ABC**，调出 Newton 原生字母键盘。
3. 输入小写全拼，例如 `ni`，再点候选字“你”提交。
4. 空格选择当前页第一个候选；单字页最多 10 项，可用数字 **1–9、0** 选择；含词语的页面最多 7 项，可用 **1–7** 选择。
5. 用候选栏的翻页按钮查看更多候选；**中／英** 切换是否使用中文候选；**X** 关闭候选栏，之后可从 Extras 重新打开。

切换到另一字段后，先确认光标位置，再点一次 **ABC** 绑定新字段。

### 中文区域、日期和时间

在 Prefs 的 Country 中选择中国后，系统可使用中文月份、星期和日期时间格式、人民币显示，以及公制和 A4 设置。需要停止使用中文区域时，在同一位置选择其他国家。区域选择不设置时区；时区仍使用 Newton 自身的城市设置。

Names 的生日、纪念日文本字段支持 `2026-10-23` 和 `2026年十月23日` 等日期输入。Dates 中的日期行继续使用原生日期选择器。输入无效日期时，应检查并改正后再保存。

### 中国地址与邮编

1. 启用中国区域，在 Names 中打开联系人的地址表单。
2. 将地址的 **Country** 填为 **China** 或 **中国**。
3. 从 **State → City → Zip Code** 依次选择省、市、区县和邮编；长列表使用 **Previous page／Next page** 翻页，也可手工填写。
4. 保存后重新打开，核对地址和邮编。

邮编按字符串保存，可保留前导零。数据来自中国邮政网点快照，使用前请核对实际投递地址。

## 4. 卸载与更换字体包

1. 保存数据，关闭 Find、日期选择器、编辑表单及 Pinyin 候选栏。
2. 按 **Pinyin IME → Chinese Region → UniBeijingX** 的顺序移除已安装的组件。
3. 更换 Lite／Full 时，移除当前字体包后先进行一次保留数据的正常重启，再按安装顺序安装所选包。

卸载组件不会主动删除已有中文记录；卸载字体后，英文 ROM 自身无法显示这些汉字。请避免在同一次开机会话中连续反复卸载、重装组件。

## 5. 已知问题与处理方法

### 错误 -10061：连续热装卸时的权限访问异常

**已知触发场景：**同一次开机会话内连续反复卸载、重装组件，尤其是在日期选择器、日期编辑或其他浮动窗口仍打开时，曾出现 `-10061`（Permission violation，权限访问异常），并导致部分区域日期方法无法正常访问。该问题尚未解决；目前确认的是上述触发场景，具体底层原因仍未查明。

**规避方法：**日常使用保持组件安装；需要移除或更换字体包时，先保存内容，关闭 Find、日期选择器、编辑表单和候选栏，按输入法、区域、字体的顺序卸载。再次安装前进行一次保留数据的正常重启，不要在多个活动窗口间连续反复热装卸。

**发生后：**停止继续装卸，保存仍可保存的内容，然后按设备的正常方式重新启动并保留原有数据；不要为此清除存储。模拟器应完全退出后使用原闪存重新启动。已有记录中，冷启动后日期功能及已保存数据恢复；这不表示故障已被修复。再次发生时，请记录错误码和触发前的操作。

### 其他限制

- **极快切换字段后的首键可能进入原字段。** 切换后确认光标，再点 ABC，稍候后输入。
- **部分字符仍可能显示方框。** 本包不覆盖全部 Unicode；两个字体版本的字符范围相同。请使用已覆盖字符，或改写超出字库范围的文字。
- **加载首帧可能短暂出现方框，部分“周”字底行可能裁切。** 等界面稳定后再阅读；必要时关闭并重新打开当前窗口。
- **很长的文件夹标题可能省略，超长地址可能响应较慢。** 使用较短名称；地址建议不超过 256 字符。
- **验证范围有限。** 本版已在 Newton OS 2.1 的隔离模拟器中验证；真实 MessagePad、实物打印及外部网络、传真、调制解调器和串口通信尚未完成验证。

## 6. 许可与来源

项目代码采用 **Apache License 2.0**，Copyright 2026 j10cc。字体采用 **SIL Open Font License 1.1**；词库相关材料保留 **MIT** 许可。下列附录随本手册提供完整许可和版权声明。

## 附录 A：Apache License 2.0

```text
Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```

## 附录 B：第三方材料声明


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
