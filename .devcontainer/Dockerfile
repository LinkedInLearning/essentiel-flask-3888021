ARG VARIANT="3.11"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

RUN apt-get -y update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install graphviz default-jre sqlite3