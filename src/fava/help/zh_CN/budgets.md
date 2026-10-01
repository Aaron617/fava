可以在 Beancount 账本中使用 `custom` 指令，为每个账户设置预算：

```beancount
2012-01-01 custom "budget" Expenses:Coffee       "daily"         4.00 EUR
2013-01-01 custom "budget" Expenses:Books        "weekly"       20.00 EUR
2014-02-10 custom "budget" Expenses:Groceries    "monthly"      40.00 EUR
2015-05-01 custom "budget" Expenses:Electricity  "quarterly"    85.00 EUR
2016-06-01 custom "budget" Expenses:Holiday      "yearly"     2500.00 EUR
```

设置后，Fava 的报表和图表会显示剩余预算及相关信息。

预算周期支持 `daily`（每天）、`weekly`（每周）、`monthly`（每月）、`quarterly`（每季度）和 `yearly`（每年）。一条预算会一直有效，直到同一账户出现新的预算指令。Fava 会将预算折算到每天，再根据所选日期范围累加。

因此可以灵活调整周期，例如先采用月预算，之后改用周预算。

预算会同时显示在图表和报表中。在损益表的“净利润”（Net Profit）和“支出”（Expenses）图表中，可以查看整体预算。

建议从损益表开始查看预算。“变动”（Changes）图表展示相关数据；“每月变动”（Changes (monthly)）和“每月余额”（Balances (monthly)）报表分别展示每月预算和所选期间的累计预算。
