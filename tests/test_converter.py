import pathlib
from unittest.mock import patch

import nbformat
import pytest
import yaml
from converter import (create_config_file, get_notebook_cells, read_config,
                       save_notebook)


@pytest.fixture
def notebook_cells():
    return [
        nbformat.v4.new_code_cell("print('Hello, World!')"),
        nbformat.v4.new_markdown_cell("# This is a heading"),
    ]


def test_read_config(tmp_path):
    config_file = tmp_path / "config.yml"
    config_file.write_text("text_highlighting_mode: dark")
    config = read_config(str(config_file))
    assert config["text_highlighting_mode"] == "dark"


@patch("src.colab2pdf.converter.google.colab._message")
def test_get_notebook_cells(mock_colab_message, notebook_cells):
    mock_blocking_request.return_value = {"ipynb": nbformat.v4.new_notebook(cells=notebook_cells).dict()}
    cells = get_notebook_cells()
    assert cells == notebook_cells


def test_save_notebook(tmp_path, notebook_cells):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    notebook_name = pathlib.Path("test_notebook")
    notebook_path = save_notebook(output_dir, notebook_name, notebook_cells)
    assert notebook_path.exists()
    with notebook_path.open("r") as file:
        notebook = nbformat.read(file, as_version=4)
        assert notebook.cells == notebook_cells


def test_create_config_file(tmp_path):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    config = {"text_highlighting_mode": "dark"}
    config_path = create_config_file(output_dir, config)
    assert config_path.exists()
    with config_path.open("r") as file:
        loaded_config = yaml.safe_load(file)
        assert loaded_config == config
