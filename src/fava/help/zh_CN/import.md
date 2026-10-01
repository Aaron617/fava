Fava 可以使用 Beancount 的导入系统，将外部记录半自动导入账本。如何编写导入器，请参考 [Beancount 外部数据导入文档](http://furius.ca/beancount/doc/ingest)。

可以定义变量 `HOOKS` 来指定导入后要运行的处理函数。它是一个函数列表，各函数处理由 `(filename: str, entries: list[Directive])` 二元组组成的列表。如果使用 beangulp 风格、接收 `(filename: str, entries: list[Directive], account: str, importer: Importer)` 四元组列表的处理函数，请为其添加相应的 Python 类型标注。Fava 会识别这些标注并按四元组格式调用。

将 `import-config` 设置为导入配置文件的路径，将 `import-dirs` 设置为待导入文件所在目录。若要将新记录写入主账本以外的位置，可以使用 `insert-entry`。

目前导入界面仅支持 `Transaction`（交易）、`Balance`（余额检查）和 `Note`（备注）三种记录。设置特殊元数据键 `__source__`，可以在待导入列表里展示原始内容，例如 CSV 的一行或 XML 片段。保存到账本之前，`__source__` 及所有以下划线开头的元数据键都会被移除。
