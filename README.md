# K3s Cluster Maintenance

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ansible](https://img.shields.io/badge/Ansible-Required-red.svg)](https://ansible.com)

**Enterprise-grade automated OS patching and system maintenance for K3s cluster nodes** with zero-downtime operations. This tool safely applies operating system updates, security patches, and package upgrades to your K3s nodes using a modular Ansible role architecture.

## 🎯 Quick Start

Run maintenance operations with simple commands:

```bash
# Update all worker nodes
ansible-playbook -i hosts.yml maintenance.yml --limit k3s_workers

# Update all master nodes  
ansible-playbook -i hosts.yml maintenance.yml --limit k3s_masters

# Update specific node
ansible-playbook -i hosts.yml maintenance.yml --limit node-01

# Update entire cluster
ansible-playbook -i hosts.yml maintenance.yml
```

## 🏗️ Enterprise Architecture

This tool uses a modular Ansible role-based architecture for production deployments:

### Role Structure
```
roles/
  k3s_node_maintenance/
    ├── tasks/
    │   ├── main.yml              # Main task orchestration
    │   ├── prerequisites.yml     # Pre-flight checks
    │   ├── package_checks.yml    # Update detection
    │   ├── cluster_preparation.yml # Node draining
    │   ├── package_updates.yml   # OS updates
    │   ├── debian_updates.yml    # Debian/Ubuntu specific
    │   ├── redhat_updates.yml    # RHEL/CentOS specific
    │   ├── reboot_handling.yml   # Reboot coordination
    │   └── cluster_restoration.yml # Node restoration
    ├── defaults/
    │   └── main.yml              # Default variables
    ├── handlers/
    │   └── main.yml              # Event handlers
    └── meta/
        └── main.yml              # Role metadata
```

### Group Variables
```
group_vars/
  ├── k3s_masters/main.yml      # Master-specific settings
  ├── k3s_workers/main.yml      # Worker-specific settings
  ├── os_debian/main.yml        # Debian/Ubuntu settings
  └── os_redhat/main.yml        # RHEL/CentOS settings
```

## 🚀 Features

- **🔄 Automated OS Patching**: System updates, security patches, and package upgrades
- **⚡ Zero-Downtime Operations**: Sequential node processing preserves cluster availability
- **🔍 Intelligent Detection**: Automatically skips maintenance when no updates are available
- **🛡️ Health Monitoring**: Comprehensive cluster and storage validation
- **🎛️ Control Plane Safety**: Master node handling with quorum protection
- **💾 Storage Integration**: Native Longhorn support with volume health verification
- **🔄 Reboot Management**: Smart reboot handling that adapts to node boot speeds
- **🏗️ Enterprise Ready**: Modular role architecture for scalability and customisation

## 📦 Repository Contents

| File | Description |
|------|-------------|
| `maintenance.yml` | Main playbook using enterprise role architecture |
| `hosts.yml.example` | Example inventory with group structure |
| `ansible.cfg` | Ansible configuration |
| `roles/` | Modular role architecture |
| `group_vars/` | Node type and OS-specific variables |
| `requirements.txt` | Python dependencies |

## 📋 Prerequisites

- **K3s cluster** (single or multi-node)
- **Ansible** (>= 2.9)
- **kubectl** configured for your cluster
- **SSH access** to all nodes with key-based authentication
- **jq** for JSON parsing

### Optional Components
- **Longhorn** storage system (health checks included)

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/sudo-kraken/k3s-cluster-maintenance.git
cd k3s-cluster-maintenance
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Inventory
```bash
cp hosts.yml.example hosts.yml
# Edit hosts.yml with your cluster details
```

### 4. Test Connectivity
```bash
ansible all -i hosts.yml -m ping
```

## 📚 Usage Examples

### Basic Maintenance Operations
```bash
# Update all worker nodes
ansible-playbook -i hosts.yml maintenance.yml --limit k3s_workers

# Update all master nodes
ansible-playbook -i hosts.yml maintenance.yml --limit k3s_masters

# Update specific node
ansible-playbook -i hosts.yml maintenance.yml --limit worker-01

# Update all Debian/Ubuntu nodes
ansible-playbook -i hosts.yml maintenance.yml --limit os_debian

# Update entire cluster
ansible-playbook -i hosts.yml maintenance.yml
```

### Advanced Operations
```bash
# Dry run (check mode)
ansible-playbook -i hosts.yml maintenance.yml --check

# Update with custom variables
ansible-playbook -i hosts.yml maintenance.yml -e "k3s_node_maintenance_wait_timeout=1200"

# Verbose output for debugging
ansible-playbook -i hosts.yml maintenance.yml -v

# Update specific nodes by pattern
ansible-playbook -i hosts.yml maintenance.yml --limit "*master*"
```

### Tagged Operations
Use tags to run specific phases of maintenance:

```bash
# Run only prerequisite checks
ansible-playbook -i hosts.yml maintenance.yml --tags prerequisites

# Check for available updates only
ansible-playbook -i hosts.yml maintenance.yml --tags packages,check_updates

# Run only cluster preparation (cordon/drain)
ansible-playbook -i hosts.yml maintenance.yml --tags cluster,prepare

# Run only package updates
ansible-playbook -i hosts.yml maintenance.yml --tags packages,updates

# Run only reboot handling
ansible-playbook -i hosts.yml maintenance.yml --tags reboot

# Run only cluster restoration (uncordon)
ansible-playbook -i hosts.yml maintenance.yml --tags restore

# Resume after manual reboot or failure
ansible-playbook -i hosts.yml maintenance.yml --tags resume

# OS-specific operations
ansible-playbook -i hosts.yml maintenance.yml --tags debian    # Debian/Ubuntu only
ansible-playbook -i hosts.yml maintenance.yml --tags redhat   # RHEL/CentOS only

# Longhorn-specific operations
ansible-playbook -i hosts.yml maintenance.yml --tags longhorn
```

### Recovery Operations
```bash
# Resume maintenance after reboot failure
ansible-playbook -i hosts.yml maintenance.yml --limit node-01 --tags resume

# Manual uncordon after successful maintenance
ansible-playbook -i hosts.yml maintenance.yml --limit node-01 --tags uncordon

# Re-enable Longhorn scheduling only
ansible-playbook -i hosts.yml maintenance.yml --limit node-01 --tags longhorn
```

## ⚙️ Configuration

### Role Variables

Customise behaviour through group variables:

#### Master Nodes (`group_vars/k3s_masters/main.yml`)
```yaml
k3s_node_maintenance_drain_timeout: 600
k3s_node_maintenance_wait_timeout: 1800
k3s_node_maintenance_skip_drain: true  # Masters are not drained
```

#### Worker Nodes (`group_vars/k3s_workers/main.yml`)
```yaml
k3s_node_maintenance_drain_timeout: 300
k3s_node_maintenance_wait_timeout: 600
k3s_node_maintenance_skip_drain: false
```

#### OS-Specific Settings
```yaml
# Debian/Ubuntu (group_vars/os_debian/main.yml)
k3s_node_maintenance_package_manager: apt
k3s_node_maintenance_cache_valid_time: 3600

# RHEL/CentOS (group_vars/os_redhat/main.yml)
k3s_node_maintenance_package_manager: dnf
k3s_node_maintenance_needs_restarting_available: true
```

### Inventory Structure

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

## 🛡️ Safety Features

### Intelligent Detection
- **Early Exit**: Automatically skips maintenance when no updates are available
- **Update Assessment**: Checks for available packages before cluster operations
- **Resource Preservation**: Prevents unnecessary downtime and resource usage

### Health Validation
- **Pre-flight Checks**: Validates prerequisites and cluster health
- **Node Readiness**: Ensures nodes are healthy before/after maintenance
- **Control Plane**: Validates API server and etcd health for masters
- **Storage Integration**: Checks Longhorn volume health (when available)

### Operational Safety
- **Sequential Processing**: Maintains only one node at a time
- **Drain Protection**: Workers are properly drained; masters are never drained
- **Smart Reboot Handling**: Adaptive monitoring that waits for actual state changes
- **Rollback Support**: Stops on first failure to prevent cascade issues

## 🔧 Troubleshooting

### Check Maintenance Status
```bash
# Verify what updates are available
ansible all -i hosts.yml -m package_facts

# Check cluster health
kubectl get nodes
kubectl get pods --all-namespaces

# Verify Longhorn status (if applicable)
kubectl get pods -n longhorn-system
```

### Common Issues

#### "No updates needed"
This is normal behaviour - the role intelligently skips maintenance when no packages need updating.

#### Node not ready after maintenance
```bash
# Check node status
kubectl get nodes

# Manual uncordon if needed
kubectl uncordon <node-name>
```

#### Ansible connection issues
```bash
# Test connectivity
ansible all -i hosts.yml -m ping

# Check SSH access
ssh user@node-ip
```

### Debug Mode
```bash
# Run with maximum verbosity
ansible-playbook -i hosts.yml maintenance.yml -vvv

# List all available tags
ansible-playbook -i hosts.yml maintenance.yml --list-tags

# Check specific task without running
ansible-playbook -i hosts.yml maintenance.yml --tags check_updates --check

# Resume from specific point
ansible-playbook -i hosts.yml maintenance.yml --limit node-01 --tags resume
```

## 🏷️ Tag Reference

| Tag | Description | Use Case |
|-----|-------------|----------|
| `prerequisites` | Pre-flight checks | Validate environment setup |
| `check_updates` | Package update detection | See what updates are available |
| `prepare` | Cluster preparation | Cordon/drain nodes only |
| `packages` | All package operations | Package management only |
| `updates` | Package installation | Install updates only |
| `reboot` | Reboot coordination | Reboot handling only |
| `restore` | Cluster restoration | Uncordon and restore scheduling |
| `resume` | Manual recovery | Resume after failures (includes restore) |
| `uncordon` | Node uncordoning | Restore node scheduling only |
| `debian` | Debian/Ubuntu only | OS-specific operations |
| `redhat` | RHEL/CentOS only | OS-specific operations |
| `longhorn` | Longhorn operations | Storage-specific tasks |

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This tool performs maintenance operations on your Kubernetes cluster. Always:
- Test in a non-production environment first
- Ensure you have recent backups
- Review the role tasks before deployment
- Monitor the process during execution

Use at your own risk. The authors are not responsible for any damage or data loss.

---

**Enterprise-grade K3s maintenance made simple**
