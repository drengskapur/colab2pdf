from unittest.mock import MagicMock, patch

import src.colab2pdf.widget


def test_on_convert_click_success():
    button = MagicMock()
    status_label = MagicMock()
    config = {"notebook_name": "test_notebook"}

    with patch("src.colab2pdf.converter.convert_notebook") as mock_convert_notebook:
        src.colab2pdf.widget.on_convert_click(button, status_label, config)

    mock_convert_notebook.assert_called_once_with(config)

    assert status_label.value == "🎉 Conversion completed"
    assert button.disabled == False
