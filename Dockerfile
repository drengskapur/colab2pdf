FROM us-docker.pkg.dev/colab-images/public/runtime

RUN apt-get update && apt-get install -y \
    librsvg2-bin \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN wget --quiet https://quarto.org/download/latest/quarto-linux-amd64.deb && \
    dpkg -i quarto-linux-amd64.deb && \
    quarto install tinytex --update-path --quiet && \
    rm quarto-linux-amd64.deb

WORKDIR /workspace

COPY . .

CMD ["/bin/bash"]
