# CLAUDE.md

本项目为 LangChain 中文教程 notebook 集合。

## Markdown 排版规则

编写 notebook 的 markdown cell 时：

- **行内不用反引号**：不要用 `` `xxx` `` 这种行内代码格式。
- **重要字段用加粗**：参数名、字段名、被讨论的消息类型主题（如 messages、max_tokens、start_on、ToolMessage）用 `**加粗**` 强调。
- **其余用纯文本**：具体的值（如 "last"、True）、函数名（如 count_tokens_approximately）、正文里解释性提及的代码表达式，直接写成纯文本，不加任何标记。
- **示意代码块保留**：三反引号的代码块（展示消息结构、代码示例等）照常保留。
