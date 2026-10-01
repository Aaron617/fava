本页是 Beancount 账本语法速查。完整说明见[语法文档](http://furius.ca/beancount/doc/syntax)和[速查表](http://furius.ca/beancount/doc/cheatsheet)。

Beancount 使用文本文件记录财务活动，再由程序读取、检查并生成报表。主要有三类组成部分：计量单位、账户、指令。

## 计量单位（Commodities）

单位代码全部大写，可以是货币、证券或其他可计量项目，例如 `USD`、`EUR`、`CAD`、`GOOG`、`AAPL`、`RBF1005`、`HOME_MAYST`、`AIRMILES`、`HOURS`。

## 账户（Accounts）

账户名称由冒号分隔的部分组成，每部分以大写字母开头。第一个部分必须是下表五个根账户之一。冒号同时定义层级，例如 `Assets:Cash` 是 `Assets` 的子账户。

| 根账户 | 中文 | 通常余额符号 | 记录什么 | 示例 |
| --- | --- | --- | --- | --- |
| `Assets` | 资产 | + | 现金、银行存款等 | `Assets:Checking` |
| `Liabilities` | 负债 | − | 信用卡欠款等 | `Liabilities:CreditCard` |
| `Income` | 收入 | − | 工资等 | `Income:EmployerA` |
| `Expenses` | 费用 | + | 各类消费费用 | `Expenses:Fun:Cinema` |
| `Equity` | 权益 | − | 期初权益等，很多记录由程序生成 | `Equity:Opening-Balances` |

这里的正负号是记账方向，不等同于“赚了”或“亏了”。例如收到工资，资产账户记正数，收入账户记负数。家庭净资产可以理解为资产减负债；Fava 的 Equity 栏包含期初权益等项目，不能简单把它的原始符号和金额当作当前净资产。

可用以下选项更改五个根账户名称。下面保留原文的德语示例，以说明配置形式；更名时账本中的账户引用也需要一致：

```beancount
option "name_assets"      "Vermoegen"
option "name_liabilities" "Verbindlichkeiten"
option "name_income"      "Einkommen"
option "name_expenses"    "Ausgaben"
option "name_equity"      "Eigenkapital"
```

## 指令（Directives）

**指令**也称为**记录**（entry），是账本的基本单位。大多数指令依次包含日期、指令类型和该类型所需的参数。Beancount 按日期整理记录，因此输入文件中的先后顺序不决定最终日期顺序。

通用形式：`YYYY-MM-DD <directive> <arguments...>`。

### 开设和关闭账户

使用 `open` 和 `close` 指令。`open` 还可限定账户使用的币种：

```beancount
2015-05-29 open Expenses:Restaurant
; Account with some currency constraints:
2015-05-29 open Assets:Checking     USD,EUR
; ...
2016-02-23 close Assets:Checking
```

### 定义计量单位

`commodity` 声明是可选的，主要用于给某个单位添加元数据。`name` 设置说明文字，在 Fava 中把鼠标停在单位名称上即可查看；`precision` 设置显示的小数位数，覆盖从账本中自动推断的精度。

```beancount
1998-07-22 commodity AAPL
  name: "Apple Computer Inc."
  precision: 3
```

### 价格

用 `price` 为历史价格表添加价格：

```beancount
2015-04-30 price AAPL   125.15 USD
2015-05-30 price AAPL   130.28 USD
```

### 备注

`note` 给账户添加说明，不产生金额变动：

```beancount
2013-03-20 note Assets:Checking "Called to ask about rebate"
```

### 凭证

`document` 把文件关联到某个账户：

```beancount
2013-03-20 document Assets:Checking "path/to/statement.pdf"
```

### 交易

交易包括日期、状态标记、可选的交易对方、摘要和各行分录。`*` 通常表示已确认，`!` 通常表示待确认。`#tag` 是标签，`^link` 是关联标识；`id:` 是元数据。简单交易可以省略其中一行的金额，由程序推算。

```beancount
2015-05-30 * "Some narration about this transaction"
  Liabilities:CreditCard   -101.23 USD
  Expenses:Restaurant       101.23 USD

2015-05-30 ! "Cable Co" "Phone Bill" #tag ^link
  id: "TW378743437"
  Expenses:Home:Phone  87.45 USD
  Assets:Checking                 ; You may leave one amount out
```

### 分录行

每行记录一个账户的变动。下面展示普通数量、成本、价格、成本日期和分录状态标记的写法；`Account:Name` 是示意占位名称，实际使用时应换成已经声明的有效账户：

```beancount
2015-05-30 * "Example transaction with various postings"
  Account:Name   123.45 USD                           ; simple units
  Account:Name      10 GOOG {502.12 USD}              ; with cost
  Account:Name  1000.00 USD  @ 1.10 CAD               ; with price
  Account:Name      10 GOOG {502.12 USD} @ 1.10 CAD   ; with cost & price
  Account:Name      10 GOOG {502.12 USD, 2014-05-12}  ; with cost date
  ! Account:Name 123.45 USD                           ; with flag
```

### 余额检查与补差

`balance` 检查指定账户、指定币种的余额是否等于给定值。余额检查以该日期开始时为准，因此核对月末余额时，通常写次月第一天：

```beancount
2015-06-01 balance Liabilities:CreditCard  -634.30 USD
```

`pad` 会插入调整交易，使后续相应的余额检查成立：

```beancount
2015-06-01 pad Assets:Checking Equity:Opening-Balances
```

余额检查可以发现差异；补差会实际改变账本金额，两者不同。不要把来源不明的差额直接补平来代替调查。

### 事件

`event` 记录随时间变化的信息，例如所在地或地址：

```beancount
2015-06-01 event "location" "New York, USA"
2015-06-01 event "address" "123 May Street"
```

### 配置选项

完整配置项见 [Beancount 配置参考](http://furius.ca/beancount/doc/options)。例如设置账本标题：

```beancount
option "title" "My Personal Ledger"
```

### 其他指令

`pushtag` 与 `poptag` 之间的记录会自动带上指定标签：

```beancount
pushtag #trip-to-peru
; ... the given tag will be added to all entries in between the pushtag and poptag
poptag  #trip-to-peru
```

### 注释

行内注释以分号开始。不以有效指令开头的非指令文本，也可以用于组织账本；编辑后仍应检查错误页，避免把本应生效的交易误写成说明文字。

```beancount
; inline comments begin with a semi-colon
* any line not starting with a valid directive is also ignored silently
```
