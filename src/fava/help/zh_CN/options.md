可以在 Beancount 账本中添加下面这样的自定义记录，调整 Fava 的行为。选项名称和配置值需要保留原有英文写法：

```beancount
2016-06-14 custom "fava-option" "default-file"
2016-04-14 custom "fava-option" "auto-reload" "true"
2016-04-14 custom "fava-option" "currency-column" "100"
```

以下是可用的配置选项。

## language

**界面语言。默认：未设置。**

未设置时，Fava 会尝试使用浏览器语言。当前包含以下界面翻译：

- 保加利亚语：`bg`
- 加泰罗尼亚语：`ca`
- 中文：简体 `zh_CN`、繁体 `zh_TW`
- 荷兰语：`nl`
- 英语：`en`
- 芬兰语：`fi`
- 法语：`fr`
- 德语：`de`
- 韩语：`ko`
- 日语：`ja`
- 波斯语：`fa`
- 葡萄牙语：`pt`、巴西葡萄牙语 `pt_BR`
- 俄语：`ru`
- 斯洛伐克语：`sk`
- 西班牙语：`es`
- 瑞典语：`sv`
- 乌克兰语：`uk`

本分支在 `zh_CN` 下同时使用简体中文帮助。其他语言没有对应帮助译文时保留英文。

## locale

**数字显示格式。默认：未设置；若启用了 Beancount 的 `render_commas`，则默认为 `en`。**

决定数字的分组和小数点格式。例如 `1111111.33` 在 `en_IN` 下显示为 `11,11,111.33`，在 `en` 下为 `1,111,111.33`，在 `de` 下为 `1.111.111,33`。

## default-file

**编辑器默认打开的文件。**

可以指定文件名，也可以不提供文件名；省略时，默认打开包含这条配置的文件。

## default-page

**默认进入的页面。默认：`income_statement/`，即损益表。**

也可以在路径中设置筛选条件。例如 `balance_sheet/?time=year-2+-+year` 会打开资产负债表，时间范围为今年及前两年。

这里使用相对路径。最方便的做法是先在浏览器中进入目标页面，再复制地址中账本名称后面的部分。

## fiscal-year-end

**会计年度结束日。默认：`12-31`。**

格式为 `%m-%d`。设置后，时间筛选可使用 `FY2018`、`FY2018-Q3`、`fiscal_year`、`fiscal_quarter`；日期范围的起止也可以使用 `FY2018`。月份允许大于 `12`，例如让标记为 FY2018 的会计年度在 2019 年结束。

示例：

- `04-05`：英国。
- `06-30`：澳大利亚／新西兰。
- `09-30`：美国联邦政府。
- `15-31`：日本，表示次年 3 月 31 日。

更多示例见[会计年度说明](https://en.wikipedia.org/wiki/Fiscal_year)。

## indent

**缩进空格数。默认：`2`。**

## insert-entry

**新记录的插入位置。默认：未设置。**

参数是匹配账户名的正则表达式，可以配置多次。新增记录时，会将它的账户与这些规则逐一匹配；交易先使用最后一行分录的账户，如果没有匹配项，再向前尝试倒数第二行，以此类推。

找到匹配项后，在记录日期之前、日期最新的匹配配置所在位置之前插入。没有匹配规则或没有设置此选项时，插入默认文件末尾。

## auto-reload

**文件变化后自动刷新。默认：`false`。**

设为 `true` 后，检测到账本文件变化就自动刷新页面。默认只显示通知，点击通知才刷新。如果变化来自页面中的操作，例如上传凭证或新增交易，Fava 总会自动刷新。

## currency-column

**币种对齐列。默认：`61`。**

保存分录或在编辑器中执行“对齐金额”时，Fava 会尽量让币种出现在指定列。编辑器也会在该列之前显示竖向参考线。

## sidebar-show-queries

**侧边栏查询链接数量上限。默认：`5`。**

设为 `0` 可隐藏这些链接。

## upcoming-events

**即将发生的事件提醒天数。默认：`7`。**

侧边栏会显示距离发生时间小于此天数的事件数量。设为 `0` 可关闭提醒。

## show-closed-accounts

**是否显示已关闭账户。默认：`false`。**

## show-accounts-with-zero-transactions

**是否显示没有交易的账户。默认：`true`。**

## show-accounts-with-zero-balance

**是否显示余额为零的账户。默认：`true`。**

以上三个选项控制损益表等页面的账户树。余额不为零的账户始终显示。

## show-metadata-indicators

**是否显示元数据标记。默认：`true`。**

在日记账的标记栏中，交易或分录行的每个元数据键都会显示一个小徽标，内容为键名的前两个字符。鼠标悬停时可以看到完整键名和值。设为 `false` 可隐藏。

## collapse-pattern

**默认折叠的账户。默认：未设置。**

参数是匹配账户名的正则表达式，可以配置多次。例如 `.*:.*:.*` 可折叠三层深度的账户及其下级内容。

## use-external-editor

**是否使用外部编辑器。默认：`false`。**

设为 `true` 后，通过 `beancount://` 链接打开外部编辑器，替代内置编辑器。配置方式见 [Beancount urlscheme](https://github.com/aumayr/beancount_urlscheme)。

## account-journal-include-children

**账户明细是否包含子账户。默认：`true`。**

决定账户报表中的日记账是否同时显示子账户的记录。

## uptodate-indicator-grey-lookback-days

**账户核对状态变灰的天数。默认：`60`。**

距最后一条余额记录超过指定天数且没有新的活动时，账户状态指示会变灰。

## import-config

**导入配置文件路径。默认：未设置。**

填写 Beancount 导入配置文件路径，详情见[导入说明](./import)。

## import-dirs

**待导入文件目录。默认：未设置。**

设置供 Beancount 导入机制扫描的目录。可以重复配置以指定多个目录。

## invert-gains-losses-colors

**是否交换浮动盈亏颜色。默认：`false`。**

资产负债表和试算表按市值显示时，默认用绿色表示未实现收益（正值），红色表示未实现损失（负值）。

设为 `true` 后改为红色表示收益、绿色表示损失，适合习惯中国股票市场配色的用户。

## invert-income-liabilities-equity

**在汇总报表中翻转收入、负债和权益的显示符号。默认：`false`。**

Beancount 的收入、负债和权益账户通常为负余额，参见[账户类型说明](https://beancount.github.io/docs/the_double_entry_counting_method/#types-of-accounts)。这是记账方向约定，不表示工资是损失，也不表示负债已经偿清。

开启此选项后，损益表和资产负债表中这三类账户的符号会翻转。对于收入大于费用的期间，净利润图也会显示正数。

例如可添加一行：`2026-01-01 custom "fava-option" "invert-income-liabilities-equity" "true"`。

**适用范围：** 为保持与账本分录一致，日记账和单个账户页面不受此选项影响。这是显示设置，不会改变账本中的交易金额。

## conversion-currencies

**币种换算下拉框的选项。默认：未设置。**

设置后，所有图表的币种换算下拉框会显示指定币种。默认列出所有主要记账币种，以及符合 ISO 4217 代码的币种。
