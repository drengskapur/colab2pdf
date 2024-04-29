import sys

if __name__ == "__main__":
    if "google.colab" in sys.modules:
        from src.colab2pdf.cli import colab2pdf_colab

        sys.exit(colab2pdf_colab())
    else:
        from src.colab2pdf.cli import colab2pdf_standalone

        sys.exit(colab2pdf_standalone(sys.argv[1:]))
