#!/usr/bin/env bash
# Install required Ansible collections for K3s maintenance

set -euo pipefail

PYTHON_VERSION="${PYTHON_VERSION:-}"
LOCK="${LOCK:-true}"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required. See https://docs.astral.sh/uv/ for installation instructions." >&2
  exit 1
fi

# Create or reuse a local venv managed by uv
if [[ -n "${PYTHON_VERSION}" ]]; then
  uv venv --python "${PYTHON_VERSION}"
else
  uv venv
fi

# Install Python dependencies from pyproject.toml and uv.lock when present
if [[ -f "pyproject.toml" ]]; then
  if [[ "${LOCK}" == "true" && -f "uv.lock" ]]; then
    uv sync --frozen --extra ansible
  else
    uv sync --extra ansible
  fi
fi

# Install required Ansible collections
if [[ -f "collections/requirements.yml" ]]; then
  uv run ansible-galaxy collection install -r collections/requirements.yml
else
  uv run ansible-galaxy collection install kubernetes.core
fi

uv run python -c 'import sys; print("Interpreter:", sys.executable)'
uv run ansible --version
uv run ansible-galaxy --version
