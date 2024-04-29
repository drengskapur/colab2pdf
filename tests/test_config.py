import src.colab2pdf.config


def test_default_config():
    assert src.colab2pdf.config.DEFAULT_CONFIG == {
        "text_highlighting_mode": src.colab2pdf.config.TextHighlightingMode.LIGHT,
        "output_format": src.colab2pdf.config.PandocOutputFormat.PDF,
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
    assert src.colab2pdf.config.TextHighlightingMode.LIGHT.value == "light"
    assert src.colab2pdf.config.TextHighlightingMode.DARK.value == "dark"
    assert src.colab2pdf.config.TextHighlightingMode.NONE.value == "none"


def test_pandoc_output_format_enum():
    assert src.colab2pdf.config.PandocOutputFormat.PDF.value == "pdf"
    assert src.colab2pdf.config.PandocOutputFormat.HTML.value == "html"
    assert src.colab2pdf.config.PandocOutputFormat.DOCX.value == "docx"
    assert src.colab2pdf.config.PandocOutputFormat.EPUB.value == "epub"
    assert src.colab2pdf.config.PandocOutputFormat.LATEX.value == "latex"
    assert src.colab2pdf.config.PandocOutputFormat.MARKDOWN.value == "markdown"
