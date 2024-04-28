from unittest.mock import MagicMock, patch

from src.colab2pdf.widget import on_convert_click


@patch("src.colab2pdf.converter.convert_notebook")
def test_on_convert_click_success(mock_convert_notebook):
    button = MagicMock()
    status_label = MagicMock()
    config = {}

    on_convert_click(button, status_label, config)

    status_label.value = "⚙️ Converting..."
    button.disabled = True

    mock_convert_notebook.assert_called_once()

    status_label.value = "🎉 Conversion completed"
    button.disabled = False


@patch("src.colab2pdf.converter.convert_notebook", side_effect=Exception("Test error"))
def test_on_convert_click_failure(mock_convert_notebook):
    button = MagicMock()
    status_label = MagicMock()
    config = {}

    on_convert_click(button, status_label, config)

    status_label.value = "⚙️ Converting..."
    button.disabled = True
    mock_convert_notebook.assert_called_once()
    status_label.value = "⚠️ ERROR Test error"
    button.disabled = False
