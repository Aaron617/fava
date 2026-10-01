Fava 支持扩展。扩展可以注册事件处理函数（hooks），也可以生成自己的报表页面。

如果现有扩展机制不能满足需要，或需要新的事件接口，可以在 [GitHub](https://github.com/beancount/fava/issues) 提出建议。

一个 Fava 扩展就是一个 Python 模块，其中包含继承自 `fava.ext.FavaExtensionBase` 的类。在 Beancount 文件中用 `fava-extension` 启用。可以参考 `fava.ext.auto_commit` 示例。

扩展类定义 `report_title` 属性时，Fava 会将它识别为带有报表页面的扩展。报表模板放在 `templates` 子目录中，文件名与类名相同。例如，`fava.ext.portfolio_list` 的模板位于 `fava/ext/portfolio_list/templates/PortfolioList.html`。

扩展还可以包含供前端加载的 JavaScript 模块：文件名应与类名相同，并将类属性 `has_js_module` 设为 `True`。模块可以定义在不同事件发生时调用的函数。示例见 `fava/ext/portfolio_list/PortfolioList.js`。目前支持：

- `init`：首次打开 Fava 报表时调用。
- `onPageLoad`：每次加载 Fava 页面时调用，包括首次打开和后续页面切换。
- `onExtensionPageLoad`：加载该扩展的报表页面时调用。

扩展模块的类型定义位于 [extension-api.d.ts](https://github.com/beancount/fava/blob/main/frontend/src/extension-api.d.ts)。可以将这份定义纳入自己的扩展，用于 TypeScript 类型检查。

整个扩展系统仍属于不稳定接口，后续版本可能有较大变化。

## 扩展配置

## `fava-extension`

指定要加载的 Python 扩展模块。除了 Python 模块搜索路径，Fava 也会搜索账本文件所在目录。单个 Python 文件同样支持：例如有 `my_extension.py` 时，可填入 `my_extension`。

Python 已加载的模块共享全局命名空间，因此应避免使用可能与其他库冲突的简单名称。同时运行两份账本、各自包含同名但不同内容的扩展时，也要注意这个问题。

扩展可以接收一个可选的配置字符串；字符串格式由各扩展自行规定。

```beancount
2010-01-01 custom "fava-extension" "extension-name"
2010-01-01 custom "fava-extension" "extension-with-options" "{'option': 'config_value'}"
```

## 事件处理函数（Hooks）

以下是目前支持的事件接口。

### `after_load_file()`

账本文件加载完成后调用。通过 `self.ledger` 访问账本数据。

### `before_request()`

开始处理一个请求时调用。可以通过 Flask 的 `request` 对象访问当前请求：`from flask import request`。

### `after_write_source(path: str, source: str)`

字符串 `source` 写入 `path` 指向的 Beancount 文件后调用。

### `after_insert_metadata(entry: Directive, key: str, value: str)`

向记录 `entry` 添加元数据 `key: value` 后调用。

### `after_insert_entry(entry: Directive)`

插入一条记录后调用。

### `after_entry_modified(entry: Directive, new_lines: str)`

修改一条记录后调用，例如通过交易详情弹窗修改。

### `after_delete_entry(entry: Directive)`

删除一条记录后调用，例如通过交易详情弹窗删除。

## 扩展属性

### `report_title`

可选属性，用于设置扩展在侧边栏中显示的报表标题。
