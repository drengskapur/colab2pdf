import pathlib
import subprocess
import tempfile

import yaml


def convert_notebook_to_pdf(notebook_content, config):
    """
    Convert the notebook content to PDF using Quarto.

    :param notebook_content: The content of the notebook.
    :type notebook_content: str
    :param config: The configuration dictionary.
    :type config: dict
    :return: The path to the generated PDF.
    :rtype: pathlib.Path
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = pathlib.Path(tmp_dir)
        notebook_path = tmp_dir_path / "notebook.ipynb"
        with open(notebook_path, "w") as file:
            file.write(notebook_content)

        config_path = tmp_dir_path / "config.yaml"
        with open(config_path, "w") as file:
            yaml.dump(config, file)

        quarto_command = [
            "quarto",
            "render",
            str(notebook_path),
            "--to",
            config["output_format"].value,
            "--metadata-file",
            str(config_path),
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

        if config["quiet"]:
            quarto_command.append("--quiet")
        elif config["verbose"]:
            quarto_command.extend(["--verbose", "--trace"])

        subprocess.run(quarto_command, check=True)
        pdf_filename = f'notebook.{config["output_format"].value}'
        pdf_path = tmp_dir_path / pdf_filename
        return pdf_path
