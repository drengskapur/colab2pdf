import pathlib
from unittest.mock import patch

from src.colab2pdf.utils import LOCAL_QUARTO_DIR, create_output_directory, get_notebook_name, is_quarto_installed


def test_is_quarto_installed(tmp_path):
    # TEST WHEN QUARTO IS NOT INSTALLED
    with patch.object(pathlib.Path, "exists", return_value=False):
        assert not is_quarto_installed()

    # TEST WHEN QUARTO IS INSTALLED
    quarto_dir = tmp_path / ".local/share/quarto"
    quarto_dir.mkdir(parents=True)
    with patch.object(pathlib.Path, "exists", return_value=True):
        assert is_quarto_installed()


@patch("requests.get")
@patch.dict("os.environ", {"COLAB_JUPYTER_IP": "127.0.0.1", "KMP_TARGET_PORT": "8888"})
def test_get_notebook_name(mock_requests_get):
    mock_requests_get.return_value.json.return_value = [{"path": "/path/to/My%20Notebook.ipynb"}]
    notebook_name = get_notebook_name()
    assert notebook_name == "My_Notebook.ipynb"


def test_create_output_directory(tmp_path):
    notebook_name = "test_notebook"
    output_dir = create_output_directory(pathlib.Path(notebook_name), tmp_path)
    assert output_dir.exists()
    assert output_dir.is_dir()
    assert output_dir.parent == tmp_path
