import enum
import pathlib
from unittest.mock import MagicMock, patch

import nbformat
import pytest
import yaml

import src.colab2pdf.config
import src.colab2pdf.converter
import src.colab2pdf.pdf_converter


@pytest.fixture
def notebook_cells():
    return [
        nbformat.v4.new_code_cell("print('Test cell 1')"),
        nbformat.v4.new_markdown_cell("# Test markdown cell"),
    ]


def test_read_config_nonexistent_file(tmp_path):
    non_existent_file = tmp_path / "nonexistent_config.yml"
    assert not non_existent_file.exists()

    config = src.colab2pdf.converter.read_config(str(non_existent_file))

    # CONVERT ENUM VALUES TO THEIR STRING REPRESENTATIONS
    default_config_str = {k: str(v.value) if isinstance(v, enum.Enum) else v for k, v in src.colab2pdf.config.DEFAULT_CONFIG.items()}
    config_str = {k: str(v.value) if isinstance(v, enum.Enum) else v for k, v in config.items()}

    assert config_str == default_config_str


def test_read_config(tmp_path):
    config_file = tmp_path / "config.yml"
    config_file.write_text("text_highlighting_mode: dark")
    config = src.colab2pdf.converter.read_config(str(config_file))
    assert config["text_highlighting_mode"] == "dark"


def test_save_notebook(tmp_path, notebook_cells):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    notebook_name = pathlib.Path("test_notebook")
    notebook_path = src.colab2pdf.converter.save_notebook(output_dir, notebook_name, notebook_cells)
    assert notebook_path.exists()
    with notebook_path.open("r") as file:
        notebook = nbformat.read(file, as_version=4)
        assert notebook.cells == notebook_cells


def test_save_notebook_with_empty_cells(tmp_path):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    notebook_name = pathlib.Path("test_notebook")
    cells = []

    notebook_path = src.colab2pdf.converter.save_notebook(output_dir, notebook_name, cells)

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
    config_path = src.colab2pdf.converter.create_config_file(output_dir, config)
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

    config_path = src.colab2pdf.converter.create_config_file(output_dir, config)

    assert config_path.exists()
    assert config_path.name == "config.yaml"

    with open(config_path) as file:
        loaded_config = yaml.safe_load(file)

    assert loaded_config == config


def test_convert_to_pdf(tmp_path):
    notebook_content = "# Test Notebook"
    config = {
        "output_format": src.colab2pdf.config.PandocOutputFormat.PDF,
        "margin_top": "1in",
        "margin_bottom": "1in",
        "margin_left": "1in",
        "margin_right": "1in",
        "quiet": False,
        "verbose": False,
    }

    with patch("subprocess.run") as mock_run:
        pdf_path = src.colab2pdf.pdf_converter.convert_notebook_to_pdf(notebook_content, config)

    expected_command = [
        "quarto",
        "render",
        str(pdf_path.parent / "notebook.ipynb"),
        "--to",
        config["output_format"].value,
        "--metadata-file",
        str(pdf_path.parent / "config.yaml"),
        "--metadata",
        "latex-auto-install",
        "--metadata",
        f'margin-top={config["margin_top"]}',
        "--metadata",
        f'margin-bottom={config["margin_bottom"]}',
        "--metadata",
        f'margin-left={config["margin_left"]}',
        "--metadata",
        f'margin-right={config["margin_right"]}',
    ]
    mock_run.assert_called_once_with(expected_command, check=True)
    assert pdf_path.name == "notebook.pdf"
