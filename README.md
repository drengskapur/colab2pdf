<img src="https://drengskapur.com/colab2pdf-banner.png" />

## Directions: Copy→Paste→Run

```python
def colab2pdf():
    # @title Colab2PDF v1.1 from [Drengskapur](https://github.com/drengskapur/colab2pdf) {display-mode:"form"}
    # License: GPL-3.0-or-later
    !apt-get install -yqq --no-install-recommends librsvg2-bin>/dev/null
    import contextlib,datetime,google,io,IPython,ipywidgets,json,locale,nbformat,os,pathlib,requests,urllib,warnings,werkzeug,yaml;locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
    def convert():
        NAME=pathlib.Path(werkzeug.utils.secure_filename(urllib.parse.unquote(requests.get(f"http://{os.environ['COLAB_JUPYTER_IP']}:{os.environ['KMP_TARGET_PORT']}/api/sessions").json()[0]["name"])))
        TMP=pathlib.Path("/content/pdfs")/f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{NAME.stem}";TMP.mkdir(parents=True,exist_ok=True);warnings.filterwarnings('ignore',category=nbformat.validator.MissingIDFieldWarning)
        NB=[cell for cell in nbformat.reads(json.dumps(google.colab._message.blocking_request("get_ipynb",timeout_sec=600)["ipynb"]),as_version=4).cells if "--Colab2PDF" not in cell.source]
        with (TMP/f"{NAME.stem}.ipynb").open("w",encoding="utf-8") as cp:nbformat.write(nbformat.v4.new_notebook(cells=NB or [nbformat.v4.new_code_cell("#")]),cp)
        if not pathlib.Path("/usr/local/bin/quarto").exists():
            !wget -q "https://quarto.org/download/latest/quarto-linux-amd64.deb" -P {TMP} && dpkg -i {TMP}/quarto-linux-amd64.deb>/dev/null && quarto install tinytex --update-path --quiet
        with (TMP/"config.yml").open("w",encoding="utf-8") as f:yaml.dump({'include-in-header':[{"text":r"\usepackage{fvextra}\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines,breakanywhere,commandchars=\\\{\}}"}],'include-before-body':[{"text":r"\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaksymbolleft={},showspaces=false,showtabs=false,breaklines}"}]},f)
        !quarto render {TMP}/{NAME.stem}.ipynb --metadata-file={TMP}/config.yml --to pdf -M latex-auto-install -M margin-top=1in -M margin-bottom=1in -M margin-left=1in -M margin-right=1in --quiet
        google.colab.files.download(str(TMP/f"{NAME.stem}.pdf"))
    def create_widget():
        download_button=ipywidgets.widgets.Button(description="⬇️ Download PDF")
        download_button.on_click(lambda b:convert())
        return IPython.display.display(ipywidgets.widgets.VBox([download_button]))
    create_widget()
colab2pdf()
```
