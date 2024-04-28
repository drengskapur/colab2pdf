from enum import Enum


class TextHighlightingMode(Enum):
    """
    Enumeration for text highlighting modes.

    :param LIGHT: Light mode.
    :type LIGHT: str
    :param DARK: Dark mode.
    :type DARK: str
    :param NONE: No highlighting.
    :type NONE: str
    """

    LIGHT = "light"
    DARK = "dark"
    NONE = "none"


class PandocOutputFormat(Enum):
    """
    Enumeration for Pandoc output formats.

    :param PDF: PDF format.
    :type PDF: str
    :param HTML: HTML format.
    :type HTML: str
    :param DOCX: DOCX format.
    :type DOCX: str
    :param EPUB: EPUB format.
    :type EPUB: str
    :param LATEX: LaTeX format.
    :type LATEX: str
    :param MARKDOWN: Markdown format.
    :type MARKDOWN: str
    """

    PDF = "pdf"
    HTML = "html"
    DOCX = "docx"
    EPUB = "epub"
    LATEX = "latex"
    MARKDOWN = "markdown"


DEFAULT_CONFIG = {
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
