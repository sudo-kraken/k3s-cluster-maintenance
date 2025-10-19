FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04@sha256:d94c97dd9cacf183d0a6fd12a8e87b526e9e928307674ae9c94139139c0c6eae

ENV DEBIAN_FRONTEND=noninteractive
ENV UV_INSTALL_DIR=/usr/local/bin
ARG UV_VERSION=0.9.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git jq \
  && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf "https://astral.sh/uv/${UV_VERSION}/install.sh" | sh

WORKDIR /workspaces/k3s-cluster-maintenance
COPY install-collections.sh /workspaces/k3s-cluster-maintenance/install-collections.sh
RUN chmod +x /workspaces/k3s-cluster-maintenance/install-collections.sh
