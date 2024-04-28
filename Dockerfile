FROM us-docker.pkg.dev/colab-images/public/runtime

# Install system dependencies
RUN apt-get update && apt-get install -y \
    librsvg2-bin \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the colab2pdf code
COPY src/ /src/

# Set the working directory
WORKDIR /src

# Install Quarto
RUN wget --quiet https://quarto.org/download/latest/quarto-linux-amd64.deb && \
    dpkg -i quarto-linux-amd64.deb && \
    quarto install tinytex --update-path --quiet && \
    rm quarto-linux-amd64.deb

# Set the default command to start a Bash session
CMD ["/bin/bash"]