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
@click.option("--config", type=click.Path(exists=True, dir_okay=False), help="Path to the configuration file (YAML)")
def convert(config):
    """
    Convert the current notebook to PDF.

    Arguments:
      --config PATH  Path to the configuration file (YAML).

    Examples:
      $ colab2pdf convert
        Convert the current notebook to PDF using default settings.

      $ colab2pdf convert --config path/to/config.yml
        Convert the current notebook to PDF using the specified configuration file.
    """
    try:
        install_dependencies()
        convert_notebook(config)
    except Exception as e:
        click.echo(f"An error occurred during conversion: {e!s}", err=True)
        raise click.ClickException(str(e))


@cli.command()
def install():
    """
    Install Quarto and its dependencies.

    Examples:
      $ colab2pdf install
        Install Quarto and its dependencies.
    """
    install_dependencies()
    install_quarto()


@cli.command()
def widget():
    """
    Launch the notebook conversion UI.

    Examples:
      $ colab2pdf widget
        Launch the notebook conversion UI.
    """
    install_dependencies()
    install_quarto()
    launch_notebook_ui()
