import __about__
import click
import config
import converter
import utils
import widget


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
        utils.install_dependencies()
        converter.convert_notebook(config)
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
    utils.install_dependencies()
    utils.install_quarto()


@cli.command()
def widget():
    """
    Launch the notebook conversion UI.

    Examples:
      $ colab2pdf widget
        Launch the notebook conversion UI.
    """
    utils.install_dependencies()
    utils.install_quarto()
    widget.launch_notebook_ui()


@click.command()
def colab2pdf_colab():
    """
    Convert the current notebook to PDF in the Google Colab environment.
    """
    converter.convert_notebook_colab(config)


@click.command()
@click.argument("notebook_path", type=click.Path(exists=True))
def colab2pdf_standalone(notebook_path):
    """
    Convert the specified notebook to PDF in a standalone environment.

    Args:
        notebook_path (str): Path to the notebook file.
    """
    converter.convert_notebook_standalone(notebook_path, config)
