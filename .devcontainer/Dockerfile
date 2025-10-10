FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Install system dependencies for Ansible and Python
RUN sudo apt update && sudo apt install -y \
	python3-pip \
	python3-venv \
	ansible \
    ansible-lint \
	curl \
	git \
	bash-completion \
	&& sudo apt clean

COPY ../install-collections.sh /workspaces/k3s-cluster-maintenance/install-collections.sh
RUN chmod +x /workspaces/k3s-cluster-maintenance/install-collections.sh
