import json
import pathlib
import warnings
from typing import List

import nbformat
import yaml
from config import DEFAULT_CONFIG
from utils import create_output_directory, get_notebook_name, install_quarto


def read_config(config_file):
    """
    Read the configuration from a YAML file.

    :param config_file: The path to the configuration file.
    :type config_file: str
    :return: The configuration dictionary.
    :rtype: dict
    """
    if pathlib.Path(config_file).exists():
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
            return {**DEFAULT_CONFIG, **config}
    return DEFAULT_CONFIG


def get_notebook_cells():
    """
    Get the cells of the current notebook.

    :return: A list of notebook cells.
    :rtype: List[nbformat.NotebookNode]
    """
    warnings.filterwarnings('ignore', category=nbformat.validator.MissingIDFieldWarning)
    ipynb = google.colab._message.blocking_request('get_ipynb', timeout_sec=600)['ipynb']
    notebook = nbformat.reads(json.dumps(ipynb), as_version=4)
    cells = [cell for cell in notebook.cells if '--Colab2PDF' not in cell.source]
    return cells


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
    notebook_filename = f'{notebook_name.stem}.ipynb'
    notebook_path = output_dir / notebook_filename
    notebook = nbformat.v4.new_notebook(cells=cells or [nbformat.v4.new_code_cell('#')])
    with notebook_path.open('w', encoding='utf-8') as file:
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
    config_path = output_dir / 'config.yaml'
    with config_path.open('w', encoding='utf-8') as file:
        yaml.dump(config, file)
    return config_path


def convert_to_pdf(notebook_path, config_path, output_dir, config):
    """
    Convert the notebook to a PDF using Quarto.

    :param notebook_path: The path to the notebook file.
    :type notebook_path: pathlib.Path
    :param config_path: The path to the configuration file.
    :type config_path: pathlib.Path
    :param output_dir: The output directory for the PDF.
    :type output_dir: pathlib.Path
    :param config: The configuration dictionary.
    :type config: dict
    :return: The path to the generated PDF.
    :rtype: pathlib.Path
    """
    quarto_command = [
        'quarto',
        'render',
        str(notebook_path),
        '--to',
        config['output_format'].value,
        '--metadata-file',
        str(config_path),
        '--metadata',
        'latex-auto-install',
        '--metadata',
        f'margin-top={config["margin_top"]}',
        '--metadata',
        f'margin-bottom={config["margin_bottom"]}',
        '--metadata',
        f'margin-left={config["margin_left"]}',
        '--metadata',
        f'margin-right={config["margin_right"]}',
    ]

    if config['quiet']:
        quarto_command.append('--quiet')
    elif config['verbose']:
        quarto_command.extend(['--verbose', '--trace'])

    subprocess.run(quarto_command, check=True)
    pdf_filename = f'{notebook_path.stem}.{config["output_format"].value}'
    pdf_path = output_dir / pdf_filename
    return pdf_path


def convert_notebook(config_file=None):
    """
    Convert the current notebook to PDF.

    :param config_file: The path to the configuration file.
    :type config_file: str, optional
    """
    install_quarto()

    config_data = read_config(config_file) if config_file else DEFAULT_CONFIG
    notebook_name = pathlib.Path(get_notebook_name())
    output_dir = create_output_directory(notebook_name)
    cells = get_notebook_cells()
    notebook_path = save_notebook(output_dir, notebook_name, cells)
    config_path = create_config_file(output_dir, config_data)
    pdf_path = convert_to_pdf(notebook_path, config_path, output_dir, config_data)
    print(f'PDF generated: {pdf_path}')
