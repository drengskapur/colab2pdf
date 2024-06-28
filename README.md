<img src="https://drengskapur.com/colab2pdf-banner.png" />

## Directions: Copy→Paste→Run

```python
def colab2pdf():
    # Colab2PDF by Drengskapur (https://github.com/drengskapur/colab2pdf)
    # @title Convert Colab Notebook to PDF {display-mode:'form'}
    # VERSION 1.5
    # LICENSE: GPL-3.0-or-later
    !apt-get install -yqq --no-install-recommends librsvg2-bin>/dev/null
    import contextlib, datetime, google, io, IPython, ipywidgets, json, locale, nbformat, os, pathlib, requests, urllib, warnings, werkzeug, yaml; locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    def convert(b):
        try:
            s.value = '⚙️ Converting...'; b.disabled = True; get_ipython().events.register('post_execute', lambda: IPython.display.display(IPython.display.Javascript('document.querySelectorAll("#output-footer").forEach(footer=>footer.remove());')))
            n = pathlib.Path(werkzeug.utils.secure_filename(urllib.parse.unquote(requests.get(f'http://{os.environ["COLAB_JUPYTER_IP"]}:{os.environ["KMP_TARGET_PORT"]}/api/sessions').json()[0]['name'])))
            p = pathlib.Path('/content/pdfs') / f'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}_{n.stem}'; p.mkdir(parents=True, exist_ok=True); warnings.filterwarnings('ignore', category=nbformat.validator.MissingIDFieldWarning)
            nb = [cell for cell in nbformat.reads(json.dumps(google.colab._message.blocking_request('get_ipynb', timeout_sec=600)['ipynb']), as_version=4).cells if '--Colab2PDF' not in cell.source]
            nb = nbformat.v4.new_notebook(cells=nb or [nbformat.v4.new_code_cell('#')]); nbformat.validate(nb); nbformat.normalize(nb)
            nbformat.write(nb, (p / f'{n.stem}.ipynb').open('w', encoding='utf-8'))
            with (p / 'config.yml').open('w', encoding='utf-8') as f: yaml.dump({'include-in-header': [{'text': r'\usepackage{fvextra}\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines,breakanywhere,commandchars=\\\{\}}'}], 'include-before-body': [{'text': r'\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines}'}]}, f)
            !quarto render {p}/{n.stem}.ipynb --metadata-file={p}/config.yml --to pdf -M latex-auto-install -M margin-top=1in -M margin-bottom=1in -M margin-left=1in -M margin-right=1in --quiet
            google.colab.files.download(str(p / f'{n.stem}.pdf')); s.value = f'🎉 Downloaded {n.stem}.pdf'
        except Exception as e:
            s.value = f'⚠️ ERROR {str(e)}'
        finally:
            b.disabled = False
    if not pathlib.Path('/usr/local/bin/quarto').exists():
        !wget -q 'https://quarto.org/download/latest/quarto-linux-amd64.deb' && dpkg -i quarto-linux-amd64.deb>/dev/null && quarto install tinytex --update-path --quiet && rm quarto-linux-amd64.deb
    b = ipywidgets.widgets.Button(description='⬇️ Download PDF'); s = ipywidgets.widgets.Label(); b.on_click(lambda b: convert(b)); IPython.display.display(ipywidgets.widgets.HBox([b, s]))
    IPython.display.display(IPython.display.Javascript('document.currentScript.parentElement.closest(".output_subarea").querySelector("#output-footer > input").remove();'))
colab2pdf()
```
