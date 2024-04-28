import click
from __about__ import __version__
from converter import convert_notebook
from utils import install_dependencies, install_quarto
from widget import launch_notebook_ui


@click.group()
def cli():
    """
    Command-line interface for converting Jupyter notebooks to PDF using Quarto.
    """
    pass


@cli.command()
@click.option('--config', type=click.Path(exists=True, dir_okay=False), help='Path to the configuration file (YAML)')
def convert(config):
    """
    Convert the current notebook to PDF.

    :param config: The path to the configuration file.
    :type config: str, optional

    Examples:
        $ colab2pdf convert
        $ colab2pdf convert --config path/to/config.yml
    """
    install_dependencies()
    convert_notebook(config)


@cli.command()
def install():
    """
    Install Quarto and its dependencies.

    Examples:
        $ colab2pdf install
    """
    install_dependencies()
    install_quarto()


@cli.command()
def widget():
    """
    Launch the notebook conversion UI.

    Examples:
        $ colab2pdf widget
    """
    install_dependencies()
    install_quarto()
    launch_notebook_ui()
