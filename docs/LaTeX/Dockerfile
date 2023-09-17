FROM debian:buster

LABEL NAME==latex
LABEL VERSION=1.0.0

RUN apt-get update && \
    apt-get install -y --no-install-recommends texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra && \
    apt-get clean

WORKDIR /docs

CMD ["bash", "/docs/build_documentation.sh"]
