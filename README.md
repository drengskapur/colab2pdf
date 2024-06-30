<img src="https://drengskapur.com/colab2pdf-banner.png" />

## Directions: Copy→Paste→Run

```python
def colab2pdf():
  # @title Download Notebook in PDF Format{display-mode:'form'}
  !apt-get install -yqq --no-install-recommends librsvg2-bin>/dev/null;
  import contextlib,datetime,google,io,IPython,ipywidgets,json,locale,nbformat,os,pathlib,requests,urllib,warnings,werkzeug,yaml,re;locale.setlocale(locale.LC_ALL,'en_US.UTF-8');warnings.filterwarnings('ignore',category=nbformat.validator.MissingIDFieldWarning);
  %matplotlib inline
  def convert(b):
    try:
      s.value='🔄 Converting';b.disabled=True
      n=pathlib.Path(werkzeug.utils.secure_filename(urllib.parse.unquote(requests.get(f'http://{os.environ["COLAB_JUPYTER_IP"]}:{os.environ["KMP_TARGET_PORT"]}/api/sessions').json()[0]['name'])))
      p=pathlib.Path('/content/pdfs')/f'{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}_{n.stem}';p.mkdir(parents=True,exist_ok=True);nb=nbformat.reads(json.dumps(google.colab._message.blocking_request('get_ipynb',timeout_sec=600)['ipynb']),as_version=4)
      u=[u for c in nb.cells if c.get('cell_type')=='markdown' for u in re.findall(r'!\[.*?\]\((https?://.*?)\)',c['source']) if requests.head(u,timeout=5).status_code!=200]
      if u:raise Exception(f"Bad Image URLs: {','.join(u)}")
      nb.cells=[cell for cell in nb.cells if '--Colab2PDF' not in cell.source]
      nb=nbformat.v4.new_notebook(cells=nb.cells or [nbformat.v4.new_code_cell('#')]);nbformat.validator.normalize(nb)
      nbformat.write(nb,(p/f'{n.stem}.ipynb').open('w',encoding='utf-8'))
      with (p/'config.yml').open('w', encoding='utf-8') as f: yaml.dump({'include-in-header':[{'text':r'\usepackage{fvextra}\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines,breakanywhere,commandchars=\\\{\}}'}],'include-before-body':[{'text':r'\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines}'}]},f)
      !quarto render {p}/{n.stem}.ipynb --metadata-file={p}/config.yml --to pdf -M latex-auto-install -M margin-top=1in -M margin-bottom=1in -M margin-left=1in -M margin-right=1in --quiet
      google.colab.files.download(str(p/f'{n.stem}.pdf'));s.value=f'✅ Downloaded: {n.stem}.pdf'
    except Exception as e:s.value=f'❌ {str(e)}'
    finally:b.disabled=False
  if not pathlib.Path('/usr/local/bin/quarto').exists():
    !wget -q 'https://quarto.org/download/latest/quarto-linux-amd64.deb' && dpkg -i quarto-linux-amd64.deb>/dev/null && quarto install tinytex --update-path --quiet && rm quarto-linux-amd64.deb
  b=ipywidgets.widgets.Button(description='⬇️ Download');s=ipywidgets.widgets.Label();b.on_click(lambda b:convert(b));IPython.display.display(ipywidgets.widgets.HBox([b,s]))
colab2pdf() # | Colab2PDF v1.6 | https://github.com/drengskapur/colab2pdf | GPL-3.0-or-later |
```

## Code Breakdown

### Importing Libraries and Setting Up Environment

```python
def colab2pdf():
    """Download Google Colab notebook as a PDF.
    colab2pdf installs dependencies, converts notebook to PDF, and provides a download link.
    """
    # Install necessary system package for PDF conversion
    !apt-get install -yqq --no-install-recommends librsvg2-bin > /dev/null  # Install librsvg2-bin for SVG conversion

    # Import necessary libraries
    import contextlib  # Provides utilities for working with context managers
    import datetime   # Supplies classes for manipulating dates and times
    import google     # Google Colab specific utilities
    import io         # Core tools for working with streams
    import IPython    # Interactive computing tools
    import ipywidgets # Interactive widgets for Jupyter notebooks
    import json       # JSON encoder and decoder
    import locale     # Internationalization services
    import nbformat   # Jupyter notebook format
    import os         # Miscellaneous operating system interfaces
    import pathlib    # Object-oriented filesystem paths
    import requests   # HTTP library for Python
    import urllib     # URL handling modules
    import warnings   # Warning control
    import werkzeug   # Comprehensive WSGI web application library
    import yaml       # YAML parser and emitter
    import re         # Regular expression operations

    # Set locale to US English
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Ensure consistent formatting

    # Ignore specific warnings
    warnings.filterwarnings('ignore', category=nbformat.validator.MissingIDFieldWarning)  # Ignore nbformat warnings

    # Enable inline plotting for matplotlib
    %matplotlib inline  # Enable inline plotting
```

1. **System Package Installation:**
   - The `librsvg2-bin` package is installed using `apt-get`. This package is necessary for converting SVG images to PDF. Without this package, SVG images in the notebook will cause errors during the PDF conversion process.

1. **Importing Libraries:**
   - Various Python libraries are imported:
     - `contextlib`: Provides utilities for working with context managers.
     - `datetime`: Supplies classes for manipulating dates and times.
     - `google`: Google Colab specific utilities.
     - `io`: Core tools for working with streams.
     - `IPython`: Interactive computing tools.
     - `ipywidgets`: Interactive widgets for Jupyter notebooks.
     - `json`: JSON encoder and decoder.
     - `locale`: Internationalization services.
     - `nbformat`: Jupyter notebook format.
     - `os`: Miscellaneous operating system interfaces.
     - `pathlib`: Object-oriented filesystem paths.
     - `requests`: HTTP library for Python.
     - `urllib`: URL handling modules.
     - `warnings`: Warning control.
     - `werkzeug`: Comprehensive WSGI web application library.
     - `yaml`: YAML parser and emitter.
     - `re`: Regular expression operations.

1. **Locale Setting:**
   - The locale is set to US English to ensure consistent formatting.

1. **Warning Filtering:**
   - Specific warnings related to `nbformat` are ignored.

1. **Matplotlib Inline:**
   - Inline plotting is enabled for `matplotlib`.

### Convert Function Definition

```python
    def convert(button):
        """Convert the current notebook to PDF and provide a download link."""
        try:
            # Update button status to indicate conversion is in progress
            status_label.value = '🔄 Converting'  # Update status label
            button.disabled = True  # Disable button to prevent multiple clicks

            # Get the notebook name from the Colab session
            session_url = f'http://{os.environ["COLAB_JUPYTER_IP"]}:{os.environ["KMP_TARGET_PORT"]}/api/sessions'
            session_response = requests.get(session_url)  # Get session data
            session_data = session_response.json()  # Parse JSON response
            notebook_name = session_data[0]['name']  # Extract notebook name

            # Create a secure filename for the notebook
            secure_notebook_name = werkzeug.utils.secure_filename(urllib.parse.unquote(notebook_name))  # Secure filename
            notebook_path = pathlib.Path(secure_notebook_name)  # Create Path object

            # Create a directory for the PDF with a timestamp
            timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")  # Current timestamp
            pdf_dir = pathlib.Path('/content/pdfs') / f'{timestamp}_{notebook_path.stem}'  # PDF directory path
            pdf_dir.mkdir(parents=True, exist_ok=True)  # Create directory

            # Read the current notebook content
            notebook_data = google.colab._message.blocking_request('get_ipynb', timeout_sec=600)['ipynb']  # Get notebook data
            notebook_json = json.dumps(notebook_data)  # Convert to JSON string
            notebook = nbformat.reads(notebook_json, as_version=4)  # Read notebook

            # Check for broken image URLs in markdown cells
            broken_urls = []
            for cell in notebook.cells:
                if cell.get('cell_type') == 'markdown':  # Check markdown cells
                    urls = re.findall(r'!\[.*?\]\((https?://.*?)\)', cell['source'])  # Find image URLs
                    for url in urls:
                        if requests.head(url, timeout=5).status_code != 200:  # Check URL status
                            broken_urls.append(url)  # Add broken URL to list
            if broken_urls:
                raise Exception(f"Bad Image URLs: {', '.join(broken_urls)}")  # Raise exception for broken URLs

            # Remove cells containing '--Colab2PDF' in their source
            notebook.cells = [cell for cell in notebook.cells if '--Colab2PDF' not in cell.source]  # Filter cells
            # Removing cells containing '--Colab2PDF' in their source. This is done to ensure that the code for the colab2pdf function itself is not included in the final PDF. The string '--Colab2PDF' acts as a marker to identify and remove these cells.

            # Create a new notebook with the filtered cells
            new_notebook = nbformat.v4.new_notebook(cells=notebook.cells or [nbformat.v4.new_code_cell('#')])  # New notebook
            nbformat.validator.normalize(new_notebook)  # Normalize notebook

            # Write the new notebook to a file
            notebook_file_path = pdf_dir / f'{notebook_path.stem}.ipynb'  # Notebook file path
            with notebook_file_path.open('w', encoding='utf-8') as notebook_file:
                nbformat.write(new_notebook, notebook_file)  # Write notebook to file

            # Create a configuration file for Quarto
            config_content = {
                'include-in-header': [{
                    'text': r'\usepackage{fvextra}\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines,breakanywhere,commandchars=\\\{\}}'
                }],
                'include-before-body': [{
                    'text': r'\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines}'
                }]
            }
            config_file_path = pdf_dir / 'config.yml'  # Config file path
            with config_file_path.open('w', encoding='utf-8') as config_file:
                yaml.dump(config_content, config_file)  # Write config to file

            # Convert the notebook to PDF using Quarto
            !quarto render {notebook_file_path} --metadata-file={config_file_path} --to pdf -M latex-auto-install -M margin-top=1in -M margin-bottom=1in -M margin-left=1in -M margin-right=1in --quiet
            # Converting the notebook to PDF using Quarto with the specified configuration.

            # Provide a download link for the PDF
            pdf_file_path = pdf_dir / f'{notebook_path.stem}.pdf'  # PDF file path
            google.colab.files.download(str(pdf_file_path))  # Provide download link
            status_label.value = f'✅ Downloaded: {notebook_path.stem}.pdf'  # Update status label

        except Exception as e:
            # Handle any exceptions that occur during the conversion process
            status_label.value = f'❌ {str(e)}'  # Display error message

        finally:
            # Re-enable the button after the process is complete
            button.disabled = False  # Re-enable button
```

1. **Button Status Update:**
   - The status label is updated to indicate that the conversion is in progress.
   - The button is disabled to prevent multiple clicks during the conversion process.

1. **Get Notebook Name:**
   - The notebook name is retrieved from the Colab session using the Colab API.

1. **Create Secure Filename:**
   - A secure filename is created for the notebook using `werkzeug.utils.secure_filename` and `urllib.parse.unquote`.

1. **Create Directory for PDF:**
   - A directory is created to store the PDF, with a timestamp to ensure uniqueness.

1. **Read Notebook Content:**
   - The current notebook content is retrieved using the Colab API and read into a `nbformat` notebook object.

1. **Check for Broken Image URLs:**
   - The function checks for broken image URLs in markdown cells. If any broken URLs are found, an exception is raised. This check is necessary because broken image URLs can cause a silent error and cut off the PDF at the point of the broken image link.

1. **Remove Specific Cells:**
   - Cells containing `--Colab2PDF` in their source are removed from the notebook. This is done to ensure that the code for the `colab2pdf` function itself is not included in the final PDF. The string `--Colab2PDF` acts as a marker to identify and remove these cells.

1. **Create New Notebook:**
   - A new notebook is created with the filtered cells, and it is normalized using `nbformat.validator.normalize`.

1. **Write Notebook to File:**
    - The new notebook is written to a file in the created directory.

1. **Create Configuration File for Quarto:**
    - A configuration file for Quarto is created with specific settings for the PDF conversion.

1. **Convert Notebook to PDF:**
    - The notebook is converted to PDF using Quarto with the specified configuration.

1. **Provide Download Link:**
    - A download link for the PDF is provided using `google.colab.files.download`.

1. **Exception Handling:**
    - Any exceptions that occur during the conversion process are caught and displayed in the status label.

1. **Re-enable Button:**
    - The button is re-enabled after the process is complete.

### Check and Install Quarto

```python
    # Check if Quarto is installed, if not, install it
    if not pathlib.Path('/usr/local/bin/quarto').exists():
        !wget -q 'https://quarto.org/download/latest/quarto-linux-amd64.deb'  # Download Quarto
        !dpkg -i quarto-linux-amd64.deb > /dev/null  # Install Quarto
        !quarto install tinytex --update-path --quiet  # Install TinyTeX
        !rm quarto-linux-amd64.deb  # Remove Quarto package
```

1. **Check if Quarto is Installed:**
   - The function checks if Quarto is installed by verifying the existence of the Quarto binary.

1. **Download and Install Quarto:**
   - If Quarto is not installed, it is downloaded using `wget` and installed using `dpkg`.

1. **Install TinyTeX:**
   - TinyTeX is installed using Quarto to ensure LaTeX dependencies are met.

1. **Remove Quarto Package:**
   - The downloaded Quarto package is removed after installation.

### Create and Display UI Elements

```python
    # Create a button and status label for the user interface
    download_button = ipywidgets.widgets.Button(description='⬇️ Download')  # Create download button
    status_label = ipywidgets.widgets.Label()  # Create status label

    # Set the button click event to trigger the convert function
    download_button.on_click(lambda b: convert(b))  # Set button click event

    # Display the button and status label
    IPython.display.display(ipywidgets.widgets.HBox([download_button, status_label]))  # Display UI elements

# Call the function to display the download button
colab2pdf()
```

1. **Create UI Elements:**
   - A download button and a status label are created using `ipywidgets`.

1. **Set Button Click Event:**
   - The button click event is set to trigger the `convert` function.

1. **Display UI Elements:**
   - The button and status label are displayed using `IPython.display.display`.

1. **Call the Function:**
   - The `colab2pdf` function is called to display the download button and initialize the process.
