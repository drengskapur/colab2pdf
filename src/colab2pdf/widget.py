import sys

from IPython import display
from ipywidgets import widgets

import src.colab2pdf.converter
import src.colab2pdf.pdf_converter
import src.colab2pdf.utils


def on_convert_click(button, status_label, config):
    try:
        status_label.value = "⚙️ Converting..."
        button.disabled = True

        try:
            src.colab2pdf.converter.convert_notebook(config)
        except Exception as e:
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
    config = {"notebook_name": src.colab2pdf.utils.get_notebook_name()}
    convert_button.on_click(lambda _: on_convert_click(convert_button, status_label, config))
    display.display(widgets.HBox([convert_button, status_label]))
