from config import DEFAULT_CONFIG
from converter import convert_notebook
from IPython import display
from ipywidgets import widgets


def on_convert_click(button, status_label, config):
    """
    Handle the click event of the convert button.

    :param button: The convert button.
    :type button: widgets.Button
    :param status_label: The label to update with the conversion status.
    :type status_label: widgets.Label
    :param config: The configuration dictionary.
    :type config: dict
    """
    try:
        status_label.value = '⚙️ Converting...'
        button.disabled = True
        convert_notebook()
        status_label.value = '🎉 Conversion completed'
    except Exception as e:
        status_label.value = f'⚠️ ERROR {str(e)}'
    finally:
        button.disabled = False


def launch_notebook_ui():
    """
    Launch the notebook conversion UI.
    """
    config = DEFAULT_CONFIG

    convert_button = widgets.Button(description='⬇️ Download PDF')
    status_label = widgets.Label()
    convert_button.on_click(lambda _: on_convert_click(convert_button, status_label, config))

    display.display(widgets.HBox([convert_button, status_label]))
