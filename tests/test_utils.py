import pathlib
from unittest.mock import patch

from src.colab2pdf.utils import create_output_directory, get_notebook_name


@patch("requests.get")
@patch.dict("os.environ", {"COLAB_JUPYTER_IP": "127.0.0.1", "KMP_TARGET_PORT": "8888"})
def test_get_notebook_name(mock_requests_get):
    mock_requests_get.return_value.json.return_value = [{"name": "My%20Notebook.ipynb"}]
    notebook_name = get_notebook_name()
    assert notebook_name == "My_Notebook.ipynb"


@patch("src.colab2pdf.utils.create_output_directory")
def test_create_output_directory(mock_create_output_directory, tmp_path):
    mock_create_output_directory.return_value = tmp_path / "output"
    notebook_name = "test_notebook"
    output_dir = create_output_directory(pathlib.Path(notebook_name))
    assert output_dir.exists()
    assert output_dir.is_dir()
    assert output_dir.parent == tmp_path / "pdfs"
