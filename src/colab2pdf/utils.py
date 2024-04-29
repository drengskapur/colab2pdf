import datetime
import locale
import os
import pathlib
import shutil
import subprocess
import tempfile
import urllib

import requests
import werkzeug

LOCAL_QUARTO_DIR = pathlib.Path.home() / ".local/share/quarto"

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


def install_dependencies():
    """
    Install the necessary dependencies using apt-get.
    """
    subprocess.run(["apt-get", "install", "--yes", "--quiet", "--no-install-recommends", "librsvg2-bin"], check=False)


def is_quarto_installed():
    """
    Check if Quarto is installed locally.

    :return: True if Quarto is installed locally, False otherwise.
    :rtype: bool
    """
    return LOCAL_QUARTO_DIR.exists()


def download_quarto(outdir):
    """
    Download the Quarto installation package.

    :param outdir: The directory to download the package to.
    :type outdir: pathlib.Path
    """
    quarto_tarball = outdir / "quarto-linux-amd64.tar.gz"
    subprocess.run(
        [
            "wget",
            "https://quarto.org/download/latest/quarto-linux-amd64.tar.gz",
            "--output-document",
            str(quarto_tarball),
        ],
        check=True,
    )
    return quarto_tarball


def install_quarto_package(quarto_tarball):
    """
    Install the Quarto package to a local directory.

    :param quarto_tarball: The path to the Quarto installation package.
    :type quarto_tarball: pathlib.Path
    """
    try:
        shutil.unpack_archive(str(quarto_tarball), str(LOCAL_QUARTO_DIR), "gztar")
    except shutil.Error as e:
        print(f"Error unpacking Quarto package: {e}")


def install_tinytex():
    """
    Install TinyTeX using the local Quarto installation.
    """
    try:
        subprocess.run([str(LOCAL_QUARTO_DIR / "bin/quarto"), "install", "tinytex", "--update-path"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing TinyTex: {e}")


def install_quarto():
    """
    Install Quarto and its dependencies if not already installed.
    """
    if not is_quarto_installed():
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir_path = pathlib.Path(tmp_dir)
            quarto_deb_path = download_quarto(tmp_dir_path)
            install_quarto_package(quarto_deb_path)
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
    notebook_path = notebook_data["path"]
    notebook_name = os.path.basename(notebook_path)
    secure_name = werkzeug.utils.secure_filename(urllib.parse.unquote(notebook_name))
    return secure_name


def create_output_directory(notebook_name, tmp_path=None):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir_name = f"{timestamp}_{notebook_name.stem}"
    if tmp_path is None:
        tmp_path = tempfile.TemporaryDirectory()
        output_dir = pathlib.Path(tmp_path.name) / output_dir_name
    else:
        output_dir = pathlib.Path(tmp_path) / output_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
