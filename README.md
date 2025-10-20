<div align="center">
<img src="docs/assets/logo.png" align="center" width="144px" height="144px"/>

### K3s Cluster Maintenance

_A modular Ansible role and playbook that performs automated operating system patching and system maintenance on K3s cluster nodes with zero-downtime semantics. Designed for local runs or CI runners._
</div>

<div align="center">

[![Ansible](https://img.shields.io/badge/Ansible-Required-red.svg?style=for-the-badge)](https://ansible.com) [![Ansible Version](https://img.shields.io/badge/Ansible-2.14%2B-blue?logo=ansible&style=for-the-badge)](https://docs.ansible.com/) 

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

Enterprise-grade automation for K3s clusters that safely applies system updates, security patches and package upgrades across master and worker nodes without impacting availability. Operations are orchestrated through a production-ready Ansible role that handles draining, reboots and post-update restoration.

## Architecture at a glance

- Modular Ansible role with `maintenance.yml` as the entry point
- Sequential node processing for zero-downtime
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
- Zero-downtime operations via safe, sequential node handling
- Intelligent detection that exits early when no updates are required
- Health monitoring across nodes, control plane and storage
- Native Longhorn integration with volume health verification and recovery waits
- Control plane safety with quorum-aware master handling
- Smart reboot management that adapts to node boot speeds
- Enterprise-ready modular role for scalability and customisation

## Prerequisites

- K3s cluster, single or multi-node
- Ansible 2.9 or newer, tested with 2.14.x
- kubectl configured for your cluster
- SSH access to all nodes with key-based authentication
- `kubernetes.core` Ansible collection
- Python Kubernetes client for API operations

## Quick start

Run maintenance using simple Ansible commands:

```bash
# Update all worker nodes
ansible-playbook -i hosts.yml maintenance.yml --limit k3s_workers

# Update all master nodes
ansible-playbook -i hosts.yml maintenance.yml --limit k3s_masters

# Update a specific node
ansible-playbook -i hosts.yml maintenance.yml --limit node-01

# Update the entire cluster
ansible-playbook -i hosts.yml maintenance.yml
```

## Configuration

### Role variables

Customise behaviour through group variables.

```yaml
# group_vars/k3s_masters/main.yml
k3s_node_maintenance_drain_timeout: 600
k3s_node_maintenance_wait_timeout: 1800
k3s_node_maintenance_skip_drain: true  # Masters are not drained

# group_vars/k3s_workers/main.yml
k3s_node_maintenance_drain_timeout: 300
k3s_node_maintenance_wait_timeout: 600
k3s_node_maintenance_skip_drain: false

# group_vars/os_debian/main.yml
k3s_node_maintenance_package_manager: apt
k3s_node_maintenance_cache_valid_time: 3600

# group_vars/os_redhat/main.yml
k3s_node_maintenance_package_manager: dnf
k3s_node_maintenance_needs_restarting_available: true
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
| `hosts.yml.example` | Example inventory with group structure |
| `ansible.cfg` | Ansible configuration |
| `roles/` | Modular role architecture |
| `group_vars/` | Node type and OS-specific variables |
| `requirements.txt` | Python dependencies |

### Tag reference

| Tag | Description | Use case |
|-----|-------------|----------|
| `prerequisites` | Pre-flight checks | Validate environment setup |
| `check_updates` | Package update detection | See what updates are available |
| `prepare` | Cluster preparation | Cordon and drain nodes only |
| `packages` | All package operations | Package management only |
| `updates` | Package installation | Install updates only |
| `reboot` | Reboot coordination | Reboot handling only |
| `restore` | Cluster restoration | Uncordon and restore scheduling |
| `resume` | Manual recovery | Resume after failures including restore |
| `uncordon` | Node uncordoning | Restore node scheduling only |
| `debian` | Debian or Ubuntu only | OS-specific operations |
| `redhat` | RHEL or CentOS only | OS-specific operations |
| `longhorn` | Longhorn operations | Storage-specific tasks |

## Health

- Pre-flight validation of cluster prerequisites and connectivity
- Node readiness checks before and after maintenance
- Control plane validation for API server and etcd on masters
- Longhorn volume health checks and recovery waits when available

## Endpoint

This project is an Ansible automation, not a network service.

- Primary entry point: `maintenance.yml`
- Invoke with `ansible-playbook -i hosts.yml maintenance.yml` and the tags or limits that fit your scenario

## Production notes

- Process nodes sequentially to preserve availability
- Keep timeouts conservative to match your node boot and image pull times
- Use `check_updates` to avoid unnecessary work when no updates are available
- When using Longhorn, allow time for degraded volumes to become healthy before proceeding
- Keep `k3s_node_maintenance_skip_drain` set appropriately for masters to protect quorum

## Development

```bash
# 1) Clone
git clone https://github.com/sudo-kraken/k3s-cluster-maintenance.git
cd k3s-cluster-maintenance

# 2) Install Python deps
pip install -r requirements.txt

# 3) Install Ansible collections
ansible-galaxy collection install kubernetes.core
# or from the file if present
ansible-galaxy collection install -r collections/requirements.yml

# 4) Configure inventory
cp hosts.yml.example hosts.yml
# edit hosts.yml with your cluster details

# 5) Test connectivity
ansible all -i hosts.yml -m ping
```

## Troubleshooting

- Verify available updates
  ```bash
  ansible all -i hosts.yml -m package_facts
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
  ansible all -i hosts.yml -m ping
  ssh user@node-ip
  ```

Debug mode

```bash
ansible-playbook -i hosts.yml maintenance.yml -vvv
ansible-playbook -i hosts.yml maintenance.yml --list-tags
ansible-playbook -i hosts.yml maintenance.yml --tags check_updates --check
ansible-playbook -i hosts.yml maintenance.yml --limit node-01 --tags resume
```

## Licence

This project is licensed under the MIT Licence. See the [LICENCE](LICENCE) file for details.

## Security

If you discover a security issue, please review and follow the guidance in [SECURITY.md](SECURITY.md) if present, or open a private security-focused issue with minimal details and request a secure contact channel.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions or improvements.
See [CONTRIBUTING.md](CONTRIBUTING.md)

## Support

Open an [issue](/../../issues) with as much detail as possible, including your Ansible version, distribution details and relevant playbook output.

## Disclaimer

This tool performs maintenance operations on your Kubernetes cluster. Always:
- Test in a non-production environment first
- Ensure you have recent backups
- Review the role tasks before deployment
- Monitor the process during execution

Use at your own risk. I am not responsible for any damage or data loss.
