#!/usr/bin/env bash

rm -rf combined.txt

find . -type f \
    -not -path "./.env" \
    -not -path "./.git/*" \
    -not -path "./.gitattributes" \
    -not -path "./.gitignore" \
    -not -path "./.vscode/extensions.json" \
    -not -path "./archive/*" \
    -not -path "./dist/*" \
    -not -path "./LICENSE.txt" \
    -not -path "./print.sh" \
    -not -path "*.pyc" \
    -exec bash -c 'echo -e "\n---\n$(dirname {})/$(basename {})\n\n" >> combined.txt; cat {} >> combined.txt' \;
