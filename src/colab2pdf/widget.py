import sys

from IPython import display
from ipywidgets import widgets

from converter import convert_notebook
from utils import get_notebook_name


def on_convert_click(button, status_label, config):
    try:
        status_label.value = "⚙️ Converting..."
        button.disabled = True

        try:
            convert_notebook(config["notebook_name"])
        except ValueError as e:
            if "expected str, bytes or os.PathLike object, not dict" in str(e):
                error_message = "Invalid file path or name provided."
            else:
                error_message = str(e)
            print(f"Error: {error_message}", file=sys.stderr)
            status_label.value = f"⚠️ ERROR: {error_message}"
        else:
            status_label.value = "🎉 Conversion completed"
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        status_label.value = f"⚠️ ERROR: {e!s}"
    finally:
        button.disabled = False


def launch_notebook_ui():
    """
    Launch the notebook conversion UI.
    """
    convert_button = widgets.Button(description="⬇️ Download PDF")
    status_label = widgets.Label()
    config = {"notebook_name": get_notebook_name()}
    convert_button.on_click(lambda _: on_convert_click(convert_button, status_label, config))
    display.display(widgets.HBox([convert_button, status_label]))
