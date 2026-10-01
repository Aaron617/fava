欢迎使用 Fava 中文帮助！当前运行的版本是 Beancount `BEANCOUNT_VERSION` 和 Fava `FAVA_VERSION`（[版本更新记录](https://beancount.github.io/fava/changelog.html)）。

**第一次使用，可以按这个顺序阅读：**

1. 打开[功能说明](./features)，了解查看账目、编辑交易和添加凭证。
2. 阅读[筛选记录](./filters)，学习按月份、账户、商家和标签查账。
3. 遇到英文账户名或金额正负号时，查看[账本语法中的账户说明](./beancount_syntax#accounts)。

**常见名词对照**

| 界面名词 | 中文含义 | 家庭记账中的例子 |
| --- | --- | --- |
| Assets | 资产 | 银行存款、钱包余额、投资 |
| Liabilities | 负债 | 信用卡欠款、贷款 |
| Income | 收入 | 工资、利息 |
| Expenses | 费用 | 吃饭、房租、交通 |
| Equity | 权益 | 期初权益等；会计等式中的权益等于资产减负债 |
| Journal | 日记账 | 逐笔交易及其他账本记录 |
| Balance Sheet | 资产负债表 | 某个时点的资产、负债与权益 |
| Income Statement | 损益表 | 某段时间的收入与费用，家庭可理解为收支表 |
| Posting | 分录行 | 一笔交易中某个账户的增减 |
| Balance assertion | 余额检查 | 核对账本余额与银行等外部记录是否一致 |

**收入为什么可能显示负数？** Beancount 用带符号的金额表示复式记账的两端。例如收到工资时，存款增加为正，收入科目通常为负；这不表示工资是损失。可以开启 [`invert-income-liabilities-equity`](./options#invert-income-liabilities-equity)，在损益表和资产负债表中翻转收入、负债和权益的显示符号。日记账和单个账户页面仍保留原始符号。

**`!` 和 `*` 是什么？** 它们是账本中的交易状态标记，通常分别用于“待确认”和“已确认”。具体确认标准由记账者或导入程序约定，不能只凭标记判断银行是否已到账。修改标记本身不会核对流水、自动配对转账或保存分类规则。

全部帮助主题：

- [Beancount 账本语法](./beancount_syntax)：语法速查。
- [预算](./budgets)：按账户设置预算。
- [功能说明](./features)：详细功能与操作。
- [筛选记录](./filters)：按条件查找账目。
- [扩展](./extensions)：扩展功能与自定义报表。
- [币种与估值转换](./conversion)：按成本、市值和其他币种查看金额。
- [导入](./import)：配置账单导入。
- [配置选项](./options)：可用设置及默认值。

Fava 提供键盘快捷键，在任意页面按 <kbd>?</kbd> 可以查看。若从命令行启动，可运行 `fava --help` 查看启动选项。

发现 Fava 的问题或有改进建议，可以提交 [GitHub 问题报告](https://github.com/beancount/fava/issues)。

### 相关网站

- Fava [官方网站](https://beancount.github.io/fava/)和 [GitHub 仓库](https://github.com/beancount/fava)。
- Beancount [完整文档](http://furius.ca/beancount/doc/index)、[邮件讨论组](https://groups.google.com/g/beancount)和[问题反馈](https://github.com/beancount/beancount/issues)。
- 其他命令行记账工具：[Plain Text Accounting](http://plaintextaccounting.org)。

本页及其他中文帮助覆盖 Fava 内置文档；上述外部网站可能仍是英文。
