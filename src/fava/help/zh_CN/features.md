本页介绍 Fava 的主要功能和操作方式。

## 编辑器

[编辑器](../editor)可以修改账本源文件。用 `default-file` 指定默认打开的文件；设置了 `insert-entry` 时，光标默认会跳到该选项按日期排序后的最新一处。

编辑器支持账户名、交易对方和标签等内容的自动补全，也会标出行尾多余空格。按 Tab 会缩进当前行；如果想用 Tab 把焦点移出编辑器，请先按 Escape，再按 Tab。

## 查询

[查询页面](../query/)支持与 `bean-query` 命令类似的查询。语法说明见 [Beancount 查询语言参考](http://furius.ca/beancount/doc/query)。

如果查询结果恰好有两列，第一列是日期或字符串、第二列是持仓集合，Fava 可以生成折线图或矩形树图。例如按交易对方汇总费用：

```
SELECT
    payee,
    SUM(COST(position)) AS balance
WHERE
    account ~ 'Expenses'
GROUP BY payee
```

查询结果可以导出为文件。默认支持 CSV；安装 `excel` 可选依赖后，还可导出 XLSX 和 ODS：

```
pip3 install fava[excel]
```

## 添加交易

点击 `+` 按钮，或按快捷键 `n`，可以打开新增交易表单。`insert-entry` 可设置新交易插入账本的位置。给任意 Fava 页面地址加上 `#add-transaction`，页面加载时就会打开此表单，也可将这个地址加入书签。

标签和关联标识可直接写在摘要中，以空格分隔，例如 `narration #tag ^somelink`。如果服务以 `--read-only` 启动，写入操作会被禁用。

## 账户核对状态指示

Fava 提供彩色圆点，帮助检查账户是否及时核对。给账户的 `open` 指令添加元数据 `fava-uptodate-indication: TRUE` 后，账户名旁会出现指示：

- **绿色**：该账户最后一条记录是余额检查，且检查通过。
- **红色**：该账户最后一条记录是余额检查，但检查未通过。
- **黄色**：最后一条记录不是余额检查。

如果账户长时间没有更新，圆点会变灰，时长由 `uptodate-indicator-grey-lookback-days` 控制。此处的圆点与报表涨跌颜色、日记账 `!` 状态标记是不同的概念。

## 只显示相关账户

账户很多或层级很深时，可以用以下选项控制显示范围：

- `show-closed-accounts`：是否显示已关闭账户。
- `show-accounts-with-zero-balance`：是否显示余额为零的账户。
- `show-accounts-with-zero-transactions`：是否显示没有交易的账户。
- `collapse-pattern`：默认折叠哪些账户。

## 使用外部编辑器

设置 `use-external-editor` 后，Fava 可通过 `beancount://` 链接调用外部编辑器打开账本。macOS 和 Cygwin 的配置示例见 [Beancount urlscheme 项目](https://github.com/aumayr/beancount_urlscheme)。

## 多份账本文件

启动 Fava 时可以传入多份账本。点击左上方的账本名称，即可切换。

## 侧边栏自定义链接

如果经常使用某个带筛选条件的页面，可以在账本中添加 `custom` 指令，将它放进侧边栏：

```beancount
2016-05-04 custom "fava-sidebar-link" "Income 2014" "../income_statement?time=2014"
```

`fava-sidebar-link` 表示侧边栏链接，后面依次是显示名称和目标地址。地址既可以像示例中那样使用相对路径，也可以是绝对地址，甚至可以指向其他网站。

特殊地址 `/jump` 用于在当前页面应用新的查询参数。例如 `/jump?time=month` 会保持当前页面，并把时间条件改成本月。

## 界面语言

用 `language` 设置界面语言。未设置时，Fava 会尝试根据浏览器语言自动选择。本分支在简体中文界面中同时显示中文帮助；没有对应译文时显示英文原文。

## 上传凭证

可以把一个或多个文件拖到账户名或日记账的交易行上，作为凭证保存。

### 上传到账户

拖拽文件时，将鼠标停留在账户树的某个账户名上，账户名的背景会变蓝，表示可以放下文件。

松开后会出现弹窗，可以在上传前重命名。如果文件名不是以 `YYYY-MM-DD` 格式的日期开头，Fava 会自动加上当天日期。

文件会保存到 Beancount 凭证目录中，以账户名组织子目录。例如可以设置：`option "documents" "/Users/test/invoices"`。目录可以使用绝对路径或相对路径。

Beancount 会自动发现这些目录中的文件，并生成 `Document` 记录。

启用 `tag_discovered_documents` 插件后，自动发现的凭证会带有 `#discovered` 标签，可以在日记账中筛选：

```beancount
plugin "fava.plugins.tag_discovered_documents"
```

### 上传到交易

把文件拖到一笔交易或其中的某行分录上时，文件仍按上述规则保存，同时会向交易添加 `document` 元数据，指向该凭证文件。

拖到交易摘要上时，会采用第一行分录的账户作为子目录。

**注意：上传到交易会修改账本文件。**

启用 `link_documents` 插件后，由 Beancount 生成的凭证记录会带有 `#linked` 标签，并关联对应交易，可以在日记账中筛选：

```beancount
plugin "fava.plugins.link_documents"
```

### 导出

点击侧边栏的 ⬇ 导出按钮，可以把当前筛选后显示的记录下载为 Beancount 格式。
