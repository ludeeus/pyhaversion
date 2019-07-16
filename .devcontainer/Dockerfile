FROM python:3.7

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Custom "commands"
RUN echo 'alias test="python //workspaces/pyhaversion/setup.py test"' >> ~/.bashrc
RUN echo 'alias commands="cat //workspaces/pyhaversion/.devcontainer/commands"' >> ~/.bashrc

WORKDIR /workspace

# Set the default shell to bash instead of sh
ENV SHELL /bin/bash
