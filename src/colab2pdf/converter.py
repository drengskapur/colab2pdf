import json
import pathlib
import sys
import warnings

import nbformat
import yaml

import src.colab2pdf.config
import src.colab2pdf.pdf_converter
import src.colab2pdf.utils


def read_config(config_file):
    """
    Read the configuration from a YAML file.

    :param config_file: The path to the configuration file.
    :type config_file: str
    :return: The configuration dictionary.
    :rtype: dict
    """
    if pathlib.Path(config_file).exists():
        with open(config_file) as file:
            config = yaml.safe_load(file)
            return {**src.colab2pdf.config.DEFAULT_CONFIG, **config}
    return src.colab2pdf.config.DEFAULT_CONFIG


def save_notebook(output_dir, notebook_name, cells):
    """
    Save the notebook with the specified cells.

    :param output_dir: The output directory for the notebook.
    :type output_dir: pathlib.Path
    :param notebook_name: The name of the notebook.
    :type notebook_name: pathlib.Path
    :param cells: The cells to include in the notebook.
    :type cells: List[nbformat.NotebookNode]
    :return: The path to the saved notebook.
    :rtype: pathlib.Path
    """
    notebook_filename = f"{notebook_name.stem}.ipynb"
    notebook_path = output_dir / notebook_filename
    notebook = nbformat.v4.new_notebook(cells=cells or [nbformat.v4.new_code_cell("#")])
    with notebook_path.open("w", encoding="utf-8") as file:
        nbformat.write(notebook, file)
    return notebook_path


def create_config_file(output_dir, config):
    """
    Create the configuration file for Quarto.

    :param output_dir: The output directory for the configuration file.
    :type output_dir: pathlib.Path
    :param config: The configuration dictionary.
    :type config: dict
    :return: The path to the created configuration file.
    :rtype: pathlib.Path
    """
    config_path = output_dir / "config.yaml"
    with config_path.open("w", encoding="utf-8") as file:
        yaml.dump(config, file)
    return config_path


def convert_notebook_colab(config):
    """
    Convert the current notebook to PDF in Google Colab environment.

    :param config: The configuration dictionary.
    :type config: dict
    """
    import google.colab._message
    warnings.filterwarnings("ignore", category=nbformat.validator.MissingIDFieldWarning)
    ipynb = google.colab._message.blocking_request("get_ipynb", timeout_sec=600)["ipynb"]
    notebook_content = json.dumps(ipynb)
    pdf_path = src.colab2pdf.pdf_converter.convert_notebook_to_pdf(notebook_content, config)
    print(f"PDF generated: {pdf_path}")


def convert_notebook_standalone(notebook_path, config):
    """
    Convert the specified notebook to PDF in standalone environment.

    :param notebook_path: The path to the notebook file.
    :type notebook_path: str
    :param config: The configuration dictionary.
    :type config: dict
    """
    with open(notebook_path, "r") as file:
        notebook_content = file.read()
    pdf_path = src.colab2pdf.pdf_converter.convert_notebook_to_pdf(notebook_content, config)
    print(f"PDF generated: {pdf_path}")


def convert_notebook(config_file=None):
    """
    Convert the current notebook to PDF.

    :param config_file: The path to the configuration file.
    :type config_file: str, optional
    """
    src.colab2pdf.utils.install_quarto()
    config_data = read_config(config_file) if config_file else src.colab2pdf.config.DEFAULT_CONFIG

    if "google.colab" in sys.modules:
        import google.colab._message
        convert_notebook_colab(config_data)
    else:
        notebook_name = pathlib.Path(src.colab2pdf.utils.get_notebook_name())
        output_dir = src.colab2pdf.utils.create_output_directory(notebook_name)
        notebook_path = output_dir / f"{notebook_name.stem}.ipynb"
        convert_notebook_standalone(str(notebook_path), config_data)
