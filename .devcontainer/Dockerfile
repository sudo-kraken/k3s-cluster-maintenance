FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Install system dependencies for Ansible and Python
RUN sudo apt update && sudo apt install -y \
	python3-pip \
	python3-venv \
	ansible \
	curl \
	git \
	bash-completion \
	&& sudo apt clean

# Remove SSL cert copy step (add back if you need it)
