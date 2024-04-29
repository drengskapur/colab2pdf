from unittest.mock import MagicMock, patch

from src.colab2pdf.widget import on_convert_click


def test_on_convert_click_success():
    button = MagicMock()
    status_label = MagicMock()
    config = {"notebook_name": "test_notebook"}

    with patch("src.colab2pdf.widget.convert_notebook") as mock_convert_notebook:
        on_convert_click(button, status_label, config)

    mock_convert_notebook.assert_called_once_with(config["notebook_name"])

    assert status_label.value == "🎉 Conversion completed"
    assert button.disabled == False
