import datetime
import locale
import os
import pathlib
import subprocess
import urllib

import requests
import werkzeug

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def install_dependencies():
    """
    Install the necessary dependencies using apt-get.
    """
    subprocess.run(['apt-get', 'install', '--yes', '--quiet', '--no-install-recommends', 'librsvg2-bin'])


def is_quarto_installed():
    """
    Check if Quarto is installed.

    :return: True if Quarto is installed, False otherwise.
    :rtype: bool
    """
    return pathlib.Path('/usr/local/bin/quarto').exists()


def download_quarto():
    """
    Download the Quarto installation package.
    """
    subprocess.run(
        [
            'wget',
            '--quiet',
            'https://quarto.org/download/latest/quarto-linux-amd64.deb',
            '--directory-prefix',
            '/content/pdfs',
        ],
        check=True,
    )


def install_quarto_package():
    """
    Install the Quarto package using dpkg.
    """
    subprocess.run(['dpkg', '--install', '/content/pdfs/quarto-linux-amd64.deb'], check=True)


def install_tinytex():
    """
    Install TinyTeX using Quarto.
    """
    subprocess.run(['quarto', 'install', 'tinytex', '--update-path', '--quiet'], check=True)


def install_quarto():
    """
    Install Quarto and its dependencies if not already installed.
    """
    if not is_quarto_installed():
        download_quarto()
        install_quarto_package()
        install_tinytex()


def get_notebook_name():
    """
    Get the name of the current notebook.

    :return: The secure name of the current notebook.
    :rtype: str
    """
    notebook_session_url = f'http://{os.environ["COLAB_JUPYTER_IP"]}:{os.environ["KMP_TARGET_PORT"]}/api/sessions'
    response = requests.get(notebook_session_url)
    notebook_data = response.json()[0]
    notebook_name = notebook_data['name']
    unquoted_name = urllib.parse.unquote(notebook_name)
    secure_name = werkzeug.utils.secure_filename(unquoted_name)
    return secure_name


def create_output_directory(notebook_name):
    """
    Create the output directory for the PDF.

    :param notebook_name: The name of the notebook.
    :type notebook_name: pathlib.Path
    :return: The path to the output directory.
    :rtype: pathlib.Path
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir_name = f'{timestamp}_{notebook_name.stem}'
    output_dir = pathlib.Path('/content/pdfs') / output_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
