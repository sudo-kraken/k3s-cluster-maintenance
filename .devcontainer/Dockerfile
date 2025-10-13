FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04@sha256:ad92cae7c25cafb1e7bb5aa7520b81be85fac022ea92e404b94a11127631fae3

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
