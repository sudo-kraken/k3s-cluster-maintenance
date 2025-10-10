#!/bin/bash

task --completion bash >> /home/vscode/.bashrc

uv run ansible-galaxy install -r collections/requirements.yml
