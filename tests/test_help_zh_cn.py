"""Chinese help coverage, fallback, anchors and executable examples."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest
from markdown_it import MarkdownIt

import fava.help as help_module
from fava.help import help_page_titles
from fava.help import HELP_PAGES
from fava.help import render_help_page

if TYPE_CHECKING:
    from pathlib import Path

    from flask.testing import FlaskClient


@pytest.mark.parametrize("page", HELP_PAGES)
def test_chinese_help_preserves_anchors_and_examples(page: str) -> None:
    """Every page is translated without breaking links or code examples."""
    english = render_help_page(page)
    chinese = render_help_page(page, "zh_CN")
    assert english
    assert chinese
    assert english != chinese
    assert re.search(r"[\u4e00-\u9fff]", chinese)
    assert re.findall(r'<h\d id="([^"]+)"', chinese) == re.findall(
        r'<h\d id="([^"]+)"',
        english,
    )
    parser = MarkdownIt()
    original = help_module._HELP_DIR / f"{page}.md"
    translated = help_module._HELP_DIR / "zh_CN" / f"{page}.md"
    tokens = parser.parse(original.read_text())
    translated_tokens = parser.parse(translated.read_text())
    assert [t.content for t in tokens if t.type == "fence"] == [
        t.content for t in translated_tokens if t.type == "fence"
    ]
    assert len([t for t in tokens if t.type == "heading_open"]) == len(
        [t for t in translated_tokens if t.type == "heading_open"]
    )


@pytest.mark.parametrize(
    "locale", ["zh", "zh_CN", "zh-CN", "zh_Hans", "zh_Hans_CN"]
)
def test_chinese_help_aliases(locale: str) -> None:
    """Simplified Chinese aliases select the translated pages and titles."""
    assert "帮助首页" in help_page_titles(locale).values()
    assert "欢迎使用 Fava 中文帮助" in (
        render_help_page("_index", locale) or ""
    )


@pytest.mark.parametrize("locale", [None, "en", "de", "zh_TW", "../../other"])
def test_help_english_fallback(locale: str | None) -> None:
    """Untranslated languages use English without path interpolation."""
    assert help_page_titles(locale) == HELP_PAGES
    assert render_help_page("features", locale) == render_help_page("features")
    assert render_help_page("../../secret", locale) is None


def test_missing_translation_falls_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A future untranslated page remains available in English."""
    (tmp_path / "features.md").write_text("English fallback.")
    monkeypatch.setattr(help_module, "_HELP_DIR", tmp_path)
    assert (
        render_help_page("features", "zh_CN") == "<p>English fallback.</p>\n"
    )


def test_chinese_local_links() -> None:
    """Internal help links resolve, including original heading anchors."""
    rendered = {
        page: render_help_page(page, "zh_CN") or "" for page in HELP_PAGES
    }
    for html in rendered.values():
        for target, anchor in re.findall(
            r'href="\./([\w_]+)(?:#([^" ]+))?"', html
        ):
            assert target in rendered
            if anchor:
                assert f'id="{anchor}"' in rendered[target]


def test_api_help_uses_interface_locale(test_client: FlaskClient) -> None:
    """The actual help endpoint selects Chinese from the request language."""
    response = test_client.get(
        "/long-example/api/help",
        query_string={"page_slug": "_index"},
        headers={"Accept-Language": "zh-CN"},
    )
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert "欢迎使用 Fava 中文帮助" in data["html"]
    assert ["_index", "帮助首页"] in data["pages"]
    response = test_client.get(
        "/long-example/api/help",
        query_string={"page_slug": "_index"},
        headers={"Accept-Language": "en"},
    )
    assert ["_index", "Index"] in response.get_json()["data"]["pages"]
