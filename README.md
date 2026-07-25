<div align="center">
<img src="docs/assets/logo.png" align="center" width="144px" height="144px"/>

### K3s Cluster Maintenance

_A modular Ansible role and playbook for safe, sequential operating system patching and maintenance of K3s cluster nodes. Designed for local runs or CI runners._
</div>

<div align="center">

[![Ansible](https://img.shields.io/badge/Ansible-Required-red.svg?style=for-the-badge)](https://ansible.com) [![Ansible Version](https://img.shields.io/badge/Ansible-2.19.3%2B-blue?logo=ansible&style=for-the-badge)](https://docs.ansible.com/)

</div>

<div align="center">

[![OpenSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/sudo-kraken/k3s-cluster-maintenance?label=openssf%20scorecard&style=for-the-badge)](https://scorecard.dev/viewer/?uri=github.com/sudo-kraken/k3s-cluster-maintenance)

</div>

## Contents

- [Overview](#overview)
- [Architecture at a glance](#architecture-at-a-glance)
  - [Role structure](#role-structure)
  - [Group variables](#group-variables)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick start](#quick-start)
- [Configuration](#configuration)
  - [Role variables](#role-variables)
  - [Inventory structure](#inventory-structure)
  - [Repository contents](#repository-contents)
  - [Tag reference](#tag-reference)
- [Health](#health)
- [Endpoint](#endpoint)
- [Production notes](#production-notes)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Licence](#licence)
- [Security](#security)
- [Contributing](#contributing)
- [Support](#support)
- [Disclaimer](#disclaimer)

## Overview

Automation for K3s clusters that applies system updates and package upgrades across master and worker nodes one at a time. The role performs health checks, PDB-aware draining, reboots and post-update restoration while preserving pre-existing scheduling state.

## Architecture at a glance

- Modular Ansible role with `maintenance.yml` as the entry point
- Sequential node processing to preserve cluster availability
- Smart detection to skip when no updates are available
- Longhorn-aware storage health checks and recovery waits
- Robust reboot handling with adaptive wait logic
- Group-based configuration via `group_vars`

### Role structure

```
roles/
  k3s_node_maintenance/
    ├── tasks/
    │   ├── main.yml                 # Main task orchestration
    │   ├── prerequisites.yml        # Pre-flight checks
    │   ├── package_checks.yml       # Update detection
    │   ├── cluster_preparation.yml  # Node draining
    │   ├── package_updates.yml      # OS updates
    │   ├── debian_updates.yml       # Debian/Ubuntu specific
    │   ├── redhat_updates.yml       # RHEL/CentOS specific
    │   ├── reboot_handling.yml      # Reboot coordination
    │   └── cluster_restoration.yml  # Node restoration
    ├── defaults/
    │   └── main.yml                 # Default variables
    ├── handlers/
    │   └── main.yml                 # Event handlers
    └── meta/
        └── main.yml                 # Role metadata
```

### Group variables

```
group_vars/
  ├── k3s_masters/main.yml   # Master-specific settings
  ├── k3s_workers/main.yml   # Worker-specific settings
  ├── os_debian/main.yml     # Debian/Ubuntu settings
  └── os_redhat/main.yml     # RHEL/CentOS settings
```

## Features

- Automated OS patching: system updates, security patches and package upgrades
- Availability-preserving operations via safe, sequential node handling
- Intelligent detection that exits early when no updates are required
- Health monitoring across nodes, control plane and storage
- Native Longhorn integration with volume health verification and recovery waits
- Control plane safety through one-node-at-a-time processing and fail-fast behavior
- Smart reboot management that adapts to node boot speeds
- Enterprise-ready modular role for scalability and customisation

## Prerequisites

- K3s cluster, single or multi-node
- Python 3.12 or newer and [uv](https://docs.astral.sh/uv/)
- Ansible Core 2.19.3 or newer
- Python 3.9 or newer on each managed node
- A working Kubernetes kubeconfig on the Ansible controller
- SSH access to all nodes with key-based authentication
- Verified node host keys in the controller's SSH `known_hosts`
- `kubernetes.core` Ansible collection
- Python Kubernetes client for API operations

## Quick start

Install the project environment and Ansible collection:

```bash
uv sync --frozen --extra ansible
uv run ansible-galaxy collection install -r collections/requirements.yml
cp hosts.example.yml hosts.yml
```

Then run maintenance:

```bash
# Update all worker nodes
uv run ansible-playbook -i hosts.yml maintenance.yml --limit k3s_workers

# Update all master nodes
uv run ansible-playbook -i hosts.yml maintenance.yml --limit k3s_masters

# Update a specific node
uv run ansible-playbook -i hosts.yml maintenance.yml --limit node-01

# Update the entire cluster
uv run ansible-playbook -i hosts.yml maintenance.yml
```

## Configuration

### Role variables

Customise behaviour through group variables.

```yaml
# host_vars/node-01.yml
# Override this when the inventory alias differs from the Kubernetes Node name.
k3s_node_maintenance_kubernetes_node_name: k3s-worker-a

# Drain safely by default: respect PDBs, DaemonSets and emptyDir data.
k3s_node_maintenance_drain_timeout: 300
k3s_node_maintenance_drain_grace_period: 30
k3s_node_maintenance_drain_force: false
k3s_node_maintenance_drain_delete_emptydir_data: false

# Maintenance controls
k3s_node_maintenance_skip_if_no_updates: true
k3s_node_maintenance_force_maintenance: false
k3s_node_maintenance_skip_drain: false
k3s_node_maintenance_longhorn_enabled: true
```

### Inventory structure

Define your cluster in `hosts.yml`:

```yaml
all:
  children:
    k3s_cluster:
      children:
        k3s_masters:
          hosts:
            master-01:
              ansible_host: 10.0.0.100
            master-02:
              ansible_host: 10.0.0.101
            master-03:
              ansible_host: 10.0.0.102
        k3s_workers:
          hosts:
            worker-01:
              ansible_host: 10.0.0.150
            worker-02:
              ansible_host: 10.0.0.151
        os_debian:
          hosts:
            master-01:
            worker-01:
        os_redhat:
          hosts:
            master-02:
            master-03:
            worker-02:
```

### Repository contents

| File | Description |
|------|-------------|
| `maintenance.yml` | Main playbook using enterprise role architecture |
| `hosts.example.yml` | Example inventory with group structure |
| `ansible.cfg` | Ansible configuration |
| `roles/` | Modular role architecture |
| `group_vars/` | Node type and OS-specific variables |
| `pyproject.toml` | Python dependencies and project metadata |
| `collections/requirements.yml` | Required Ansible collections |

### Tag reference

| Tag | Description | Use case |
|-----|-------------|----------|
| `prerequisites` | Pre-flight checks | Validate environment setup |
| `check_updates` | Package update detection | See what updates are available |
| `cluster` | Cluster scheduling operations | Drain and restore nodes without package changes |
| `prepare` | Cluster preparation | Cordon and drain nodes only |
| `packages` | All package operations | Package management only |
| `updates` | Package installation | Install updates only |
| `reboot` | Reboot coordination | Reboot handling only |
| `restore` | Cluster restoration | Uncordon and restore scheduling |
| `resume` | Manual recovery | Validate readiness and optionally restore scheduling |
| `uncordon` | Node uncordoning | Restore node scheduling only |
| `debian` | Debian or Ubuntu only | OS-specific operations |
| `redhat` | RHEL or CentOS only | OS-specific operations |
| `longhorn` | Longhorn validation | Check storage health and volume recovery |

## Health

- Pre-flight validation of cluster prerequisites and connectivity
- Node readiness checks before and after maintenance
- Cluster-wide node readiness and scheduling validation
- Longhorn volume health checks and recovery waits when available

## Endpoint

This project is an Ansible automation, not a network service.

- Primary entry point: `maintenance.yml`
- Invoke with `uv run ansible-playbook -i hosts.yml maintenance.yml` and the tags or limits that fit your scenario

## Production notes

- Nodes are processed sequentially and maintenance stops on the first failure
- Keep timeouts conservative to match your node boot and image pull times
- Use `check_updates` to avoid unnecessary work when no updates are available
- When using Longhorn, allow time for degraded volumes to become healthy before proceeding
- Leave draining enabled unless you have reviewed the workload-disruption consequences
- Set `k3s_node_maintenance_kubernetes_node_name` when an inventory hostname is not the Kubernetes Node name

## Development

```bash
# 1) Clone
git clone https://github.com/sudo-kraken/k3s-cluster-maintenance.git
cd k3s-cluster-maintenance

# 2) Install Python dependencies and Ansible collections
uv sync --frozen --extra ansible
uv run ansible-galaxy collection install -r collections/requirements.yml

# 3) Configure inventory
cp hosts.example.yml hosts.yml
# edit hosts.yml with your cluster details

# 4) Test connectivity
uv run ansible all -i hosts.yml -m ping
```

## Troubleshooting

- Verify available updates
  ```bash
  uv run ansible all -i hosts.yml -m package_facts
  ```
- Check cluster health
  ```bash
  kubectl get nodes
  kubectl get pods --all-namespaces
  ```
- Verify Longhorn status if applicable
  ```bash
  kubectl get pods -n longhorn-system
  ```

Common issues

- No updates needed  
  Normal behaviour. The role skips maintenance when no packages need updating.

- Node not ready after maintenance
  ```bash
  kubectl get nodes
  kubectl uncordon <node-name>
  ```

- Ansible connection issues
  ```bash
  uv run ansible all -i hosts.yml -m ping
  ssh user@node-ip
  ```

Debug mode

```bash
uv run ansible-playbook -i hosts.yml maintenance.yml -vvv
uv run ansible-playbook -i hosts.yml maintenance.yml --list-tags
uv run ansible-playbook -i hosts.yml maintenance.yml --tags check_updates --check
uv run ansible-playbook -i hosts.yml maintenance.yml --limit node-01 --tags resume \
  -e k3s_node_maintenance_resume_restore_scheduling=true
```

## Licence

This project is licensed under the MIT Licence. See the [LICENSE](LICENSE) file for details.

## Security

If you discover a security issue, follow [SECURITY.md](SECURITY.md) and use the repository's private vulnerability reporting process. Do not open a public issue.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions or improvements.
See [CONTRIBUTING.md](CONTRIBUTING.md)

## Support

Open an [issue](https://github.com/sudo-kraken/k3s-cluster-maintenance/issues) with as much detail as possible, including your Ansible version, distribution details and relevant playbook output.

## Disclaimer

This tool performs maintenance operations on your Kubernetes cluster. Always:
- Test in a non-production environment first
- Ensure you have recent backups
- Review the role tasks before deployment
- Monitor the process during execution

Use at your own risk. I am not responsible for any damage or data loss.
