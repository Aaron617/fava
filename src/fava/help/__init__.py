"""List of all available help pages."""

from __future__ import annotations

from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING

from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from markdown_it.renderer import RendererHTML

from fava.core.fava_options import DASHED_OPTION_NAMES
from fava.util import slugify

try:
    from typing import override
except ImportError:  # pragma: no cover
    from typing_extensions import override

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Sequence

    from markdown_it.token import Token
    from markdown_it.utils import EnvType
    from markdown_it.utils import OptionsDict

HELP_PAGES = {
    "_index": "Index",
    "budgets": "Budgets",
    "conversion": "Conversion",
    "import": "Import",
    "options": "Options",
    "beancount_syntax": "Beancount Syntax",
    "features": "Features",
    "filters": "Filtering entries",
    "extensions": "Extensions",
}

HELP_PAGES_ZH_CN = {
    "_index": "帮助首页",
    "budgets": "预算",
    "conversion": "币种与估值转换",
    "import": "导入",
    "options": "配置选项",
    "beancount_syntax": "Beancount 账本语法",
    "features": "功能说明",
    "filters": "筛选记录",
    "extensions": "扩展",
}

_HELP_DIR = Path(__file__).parent


def _is_simplified_chinese(language: str | None) -> bool:
    return (language or "").replace("-", "_").lower() in {
        "zh",
        "zh_cn",
        "zh_hans",
        "zh_hans_cn",
    }


def help_page_titles(language: str | None = None) -> dict[str, str]:
    """Return help navigation titles for the requested language."""
    return HELP_PAGES_ZH_CN if _is_simplified_chinese(language) else HELP_PAGES


class _CustomRenderer(RendererHTML):
    """Some custom help pages rendering logic."""

    @override
    def code_inline(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        """Link `fava-option` references to their options help page heading."""
        rendered = super().code_inline(tokens, idx, options, env)
        name = tokens[idx].content
        if name not in DASHED_OPTION_NAMES:
            return rendered
        return f'<a href="./options#{name}">{rendered}</a>'

    def heading_open(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        """Add an id to all headings so that they can be linked to."""
        seen: set[str] = env.setdefault("heading_ids", set())
        heading_index = env.get("heading_index", 0)
        original_slugs = env.get("original_heading_slugs", [])
        slug = (
            original_slugs[heading_index]
            if heading_index < len(original_slugs)
            else slugify(tokens[idx + 1].content)
        )
        env["heading_index"] = heading_index + 1
        if slug in seen:  # pragma: no cover
            msg = f"Duplicate heading {slug}"
            raise ValueError(msg)
        seen.add(slug)
        tokens[idx].attrSet("id", slug)
        return self.renderToken(tokens, idx, options, env)

    @override
    def fence(
        self,
        tokens: Sequence[Token],
        idx: int,
        options: OptionsDict,
        env: EnvType,
    ) -> str:
        """Render ```beancount code blocks as read-only Beancount editors."""
        token = tokens[idx]
        if token.info.strip() != "beancount":
            return super().fence(tokens, idx, options, env)
        source = escapeHtml(token.content.rstrip("\n"))
        return (
            f'<pre><textarea is="beancount-textarea">{source}'
            "</textarea></pre>\n"
        )


_MD = MarkdownIt("commonmark", renderer_cls=_CustomRenderer).enable("table")


def render_help_page(
    page_slug: str,
    language: str | None = None,
) -> str | None:
    """Render the HTML for a help page."""
    if page_slug not in HELP_PAGES:
        return None

    help_path = _HELP_DIR / (page_slug + ".md")
    contents = help_path.read_text(encoding="utf-8")
    env: EnvType = {}
    if _is_simplified_chinese(language):
        translated_path = _HELP_DIR / "zh_CN" / (page_slug + ".md")
        if translated_path.is_file():
            # Keep existing deep links when translating the visible headings.
            original_tokens = _MD.parse(contents)
            env["original_heading_slugs"] = [
                slugify(original_tokens[i + 1].content)
                for i, token in enumerate(original_tokens)
                if token.type == "heading_open"
            ]
            contents = translated_path.read_text(encoding="utf-8")
    html: str = _MD.render(contents, env)
    if page_slug == "_index":
        html = html.replace("BEANCOUNT_VERSION", version("beancount"))
        html = html.replace("FAVA_VERSION", version("fava"))
    return html
