import enum
import json
import pathlib
import sys
from unittest.mock import MagicMock, patch

import nbformat
import pytest
import yaml

from src.colab2pdf.config import DEFAULT_CONFIG, PandocOutputFormat
from src.colab2pdf.converter import (
    convert_notebook,
    convert_to_pdf,
    create_config_file,
    read_config,
    save_notebook,
)

sys.modules["google.colab"] = MagicMock()
sys.modules["google.colab._message"] = MagicMock()


class MockColabMessage:
    def blocking_request(self, *args, **kwargs):
        notebook_json = {
            "cells": [
                {"source": "print('Test cell 1')", "cell_type": "code"},
                {"source": "# Test markdown cell", "cell_type": "markdown"},
            ],
            "metadata": {},
            "nbformat_minor": 0,
            "nbformat": 4,
        }
        return {"ipynb": json.dumps(notebook_json)}


@pytest.fixture(autouse=True)
def mock_google_colab():
    mock_colab_message = MockColabMessage()
    sys.modules["google"] = MagicMock()
    sys.modules["google.colab"] = MagicMock()
    sys.modules["google.colab._message"] = mock_colab_message
    yield
    del sys.modules["google"]
    del sys.modules["google.colab"]
    del sys.modules["google.colab._message"]


@pytest.fixture
def notebook_cells():
    return [
        nbformat.v4.new_code_cell("print('Test cell 1')"),
        nbformat.v4.new_markdown_cell("# Test markdown cell"),
    ]


def test_read_config_nonexistent_file(tmp_path):
    non_existent_file = tmp_path / "nonexistent_config.yml"
    assert not non_existent_file.exists()

    config = read_config(str(non_existent_file))

    # CONVERT ENUM VALUES TO THEIR STRING REPRESENTATIONS
    default_config_str = {k: str(v.value) if isinstance(v, enum.Enum) else v for k, v in DEFAULT_CONFIG.items()}
    config_str = {k: str(v.value) if isinstance(v, enum.Enum) else v for k, v in config.items()}

    assert config_str == default_config_str


def test_read_config(tmp_path):
    config_file = tmp_path / "config.yml"
    config_file.write_text("text_highlighting_mode: dark")
    config = read_config(str(config_file))
    assert config["text_highlighting_mode"] == "dark"


def test_save_notebook(tmp_path, notebook_cells):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    notebook_name = pathlib.Path("test_notebook")
    notebook_path = save_notebook(output_dir, notebook_name, notebook_cells)
    assert notebook_path.exists()
    with notebook_path.open("r") as file:
        notebook = nbformat.read(file, as_version=4)
        assert notebook.cells == notebook_cells


def test_save_notebook_with_empty_cells(tmp_path):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    notebook_name = pathlib.Path("test_notebook")
    cells = []

    notebook_path = save_notebook(output_dir, notebook_name, cells)

    assert notebook_path.exists()
    assert notebook_path.name == "test_notebook.ipynb"

    with open(notebook_path) as file:
        loaded_notebook = nbformat.read(file, as_version=4)

    assert len(loaded_notebook.cells) == 1
    assert loaded_notebook.cells[0].cell_type == "code"
    assert loaded_notebook.cells[0].source == "#"


def test_create_config_file(tmp_path):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    config = {"text_highlighting_mode": "dark"}
    config_path = create_config_file(output_dir, config)
    assert config_path.exists()
    with config_path.open("r") as file:
        loaded_config = yaml.safe_load(file)
        assert loaded_config == config


def test_create_config_file(tmp_path):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    config = {
        "text_highlighting_mode": "dark",
        "output_format": "pdf",
        "margin_top": "1in",
        "margin_bottom": "1in",
        "margin_left": "1in",
        "margin_right": "1in",
    }

    config_path = create_config_file(output_dir, config)

    assert config_path.exists()
    assert config_path.name == "config.yaml"

    with open(config_path) as file:
        loaded_config = yaml.safe_load(file)

    assert loaded_config == config


def test_convert_to_pdf(tmp_path):
    notebook_path = tmp_path / "test_notebook.ipynb"
    notebook_path.touch()
    config_path = tmp_path / "config.yaml"
    config_path.touch()
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    config = {
        "output_format": PandocOutputFormat.PDF,
        "margin_top": "1in",
        "margin_bottom": "1in",
        "margin_left": "1in",
        "margin_right": "1in",
        "quiet": False,
        "verbose": False,
    }

    expected_command = [
        "quarto",
        "render",
        str(notebook_path),
        "--to",
        "pdf",
        "--metadata-file",
        str(config_path),
        "--metadata",
        "latex-auto-install",
        "--metadata",
        "margin-top=1in",
        "--metadata",
        "margin-bottom=1in",
        "--metadata",
        "margin-left=1in",
        "--metadata",
        "margin-right=1in",
    ]

    with patch("subprocess.run") as mock_run:
        pdf_path = convert_to_pdf(notebook_path, config_path, output_dir, config)

    mock_run.assert_called_once_with(expected_command, check=True)
    assert pdf_path == output_dir / "test_notebook.pdf"


@patch("src.colab2pdf.converter.install_quarto")
@patch("src.colab2pdf.converter.get_notebook_name")
@patch("src.colab2pdf.converter.create_output_directory")
@patch("src.colab2pdf.converter.get_notebook_cells")
@patch("src.colab2pdf.converter.save_notebook")
@patch("src.colab2pdf.converter.create_config_file")
@patch("src.colab2pdf.converter.convert_to_pdf")
def test_convert_notebook_calls_expected_functions(
    mock_convert_to_pdf,
    mock_create_config_file,
    mock_save_notebook,
    mock_get_notebook_cells,
    mock_create_output_directory,
    mock_get_notebook_name,
    mock_install_quarto,
    tmp_path,
):
    notebook_name = pathlib.Path("test_notebook")
    output_dir = tmp_path / "output"
    cells = [MagicMock()]
    config_data = DEFAULT_CONFIG
    notebook_path = tmp_path / "test_notebook.ipynb"
    config_path = tmp_path / "config.yaml"
    pdf_path = tmp_path / "test_notebook.pdf"

    mock_get_notebook_name.return_value = str(notebook_name)
    mock_create_output_directory.return_value = output_dir
    mock_get_notebook_cells.return_value = cells
    mock_save_notebook.return_value = notebook_path
    mock_create_config_file.return_value = config_path
    mock_convert_to_pdf.return_value = pdf_path

    convert_notebook()

    mock_install_quarto.assert_called_once()
    mock_get_notebook_name.assert_called_once()
    mock_create_output_directory.assert_called_once_with(notebook_name)
    mock_get_notebook_cells.assert_called_once()
    mock_save_notebook.assert_called_once_with(output_dir, notebook_name, cells)
    mock_create_config_file.assert_called_once()
    mock_convert_to_pdf.assert_called_once()
