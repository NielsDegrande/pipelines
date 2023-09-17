#!/bin/bash

# Build all main.tex files in this folder.
for file in /docs/*.tex;
do
    basefile="$(basename "$file" .tex)"
    pdflatex -jobname="$basefile" "$file";
done

# Move pdf files to pdf folder.
mkdir -p /docs/pdf
mv /docs/*.pdf /docs/pdf
