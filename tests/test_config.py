from src.colab2pdf.config import DEFAULT_CONFIG, PandocOutputFormat, TextHighlightingMode


def test_default_config():
    assert DEFAULT_CONFIG == {
        "text_highlighting_mode": TextHighlightingMode.LIGHT,
        "output_format": PandocOutputFormat.PDF,
        "margin_top": "1in",
        "margin_bottom": "1in",
        "margin_left": "1in",
        "margin_right": "1in",
        "quiet": False,
        "verbose": False,
        "data_dir": "pandoc/datadir",
        "syntax_definitions_dir": "pandoc/syntax-definitions",
        "keep_yaml": False,
        "default_markdown_template": "pandoc/templates/default.markdown",
        "emoji_image_path": "quarto/emoji",
    }


def test_text_highlighting_mode_enum():
    assert TextHighlightingMode.LIGHT.value == "light"
    assert TextHighlightingMode.DARK.value == "dark"
    assert TextHighlightingMode.NONE.value == "none"


def test_pandoc_output_format_enum():
    assert PandocOutputFormat.PDF.value == "pdf"
    assert PandocOutputFormat.HTML.value == "html"
    assert PandocOutputFormat.DOCX.value == "docx"
    assert PandocOutputFormat.EPUB.value == "epub"
    assert PandocOutputFormat.LATEX.value == "latex"
    assert PandocOutputFormat.MARKDOWN.value == "markdown"
