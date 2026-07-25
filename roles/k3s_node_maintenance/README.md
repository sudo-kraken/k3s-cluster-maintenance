# K3s Node Maintenance Role

This role provides safe, sequential OS patching and maintenance for K3s cluster nodes.

## Role Variables

### Default Variables (`defaults/main.yml`)
- `k3s_node_maintenance_wait_timeout`: Maximum time to wait for node readiness (default: 600s)
- `k3s_node_maintenance_drain_timeout`: Timeout for node draining (default: 300s)
- `k3s_node_maintenance_drain_grace_period`: Grace period for pod termination (default: 30s)
- `k3s_node_maintenance_drain_force`: Drain pods without a controller (default: false)
- `k3s_node_maintenance_drain_delete_emptydir_data`: Permit deletion of `emptyDir` data (default: false)
- `k3s_node_maintenance_reboot_pause`: Initial pause after reboot initiation (default: 30s)
- `k3s_node_maintenance_apt_cache_valid_time`: APT cache validity time (default: 3600s)
- `k3s_node_maintenance_kubernetes_node_name`: Kubernetes Node name (default: inventory hostname)
- `k3s_node_maintenance_skip_if_no_updates`: Skip a current node without ending the play (default: true)
- `k3s_node_maintenance_force_maintenance`: Continue even when no updates are detected (default: false)
- `k3s_node_maintenance_skip_drain`: Skip cordon and drain operations (default: false)
- `k3s_node_maintenance_longhorn_enabled`: Enable Longhorn checks (default: true)
- `k3s_node_maintenance_resume_restore_scheduling`: Restore scheduling during a fresh resume run (default: false)

The role preserves a node's pre-existing cordon state and a Longhorn node's pre-existing scheduling state.

### Group Variables

#### `group_vars/k3s_masters/main.yml`
- Extended timeouts for master nodes
- Conservative reboot behaviour

#### `group_vars/k3s_workers/main.yml`
- Standard timeouts for worker nodes
- Standard reboot behaviour

#### `group_vars/os_debian/main.yml`
- APT cache lifetime and metadata-refresh retry settings

#### `group_vars/os_redhat/main.yml`
- DNF metadata-refresh retry settings

## Task Structure

The role is organised into logical task files:

- `tasks/main.yml`: Main orchestration
- `tasks/prerequisites.yml`: Pre-flight checks
- `tasks/package_checks.yml`: Update detection and early exit
- `tasks/longhorn_validation.yml`: Longhorn storage health checks and volume recovery
- `tasks/cluster_preparation.yml`: PDB-aware node cordoning and draining
- `tasks/package_updates.yml`: OS-specific update inclusion
- `tasks/debian_updates.yml`: Debian/Ubuntu package updates
- `tasks/redhat_updates.yml`: RHEL/CentOS package updates
- `tasks/reboot_handling.yml`: Smart reboot coordination with adaptive monitoring
- `tasks/cluster_restoration.yml`: Node restoration
- `tasks/final_validation.yml`: Post-maintenance cluster health validation
- `tasks/resume_after_reboot.yml`: Manual recovery after reboot issues

## Tags

All tasks are tagged for granular control:

### Main Phase Tags
- `prerequisites`: Pre-flight checks and tool validation
- `packages`: All package-related operations
- `cluster`: All cluster management operations (cordon/drain/uncordon)
- `reboot`: Reboot coordination and monitoring
- `restore`: Cluster restoration (uncordon, Longhorn re-enable)
- `resume`: Manual recovery after reboot failures

### Specific Operation Tags
- `check_updates`: Package update detection only
- `prepare`: Cluster preparation (cordon/drain)
- `updates`: Package installation only
- `uncordon`: Node uncordoning only
- `longhorn`: Longhorn-specific operations (health checks, volume recovery)
- `health`: Health validation and storage checks
- `validation`: Pre/post maintenance validation
- `wait`: Volume recovery waiting operations

### OS-Specific Tags
- `debian`: Debian/Ubuntu operations only
- `redhat`: RHEL/CentOS operations only

### Example Tag Usage
```bash
# Check what updates are available
ansible-playbook -i hosts.yml maintenance.yml --tags check_updates

# Only prepare cluster (no updates)
ansible-playbook -i hosts.yml maintenance.yml --tags prepare

# Resume after manual reboot
ansible-playbook -i hosts.yml maintenance.yml --tags resume \
  -e k3s_node_maintenance_resume_restore_scheduling=true
```

## Dependencies

- Ansible Core 2.19.3 or newer
- `kubernetes.core` collection
- Python Kubernetes client on the controller
- Python 3.9 or newer on managed nodes

## Example Playbook

```yaml
---
- name: K3s Cluster Node Maintenance
  hosts: "{{ target | default('k3s_cluster') }}"
  gather_facts: false
  serial: 1
  any_errors_fatal: true
  roles:
    - k3s_node_maintenance
```

## Inventory Groups

The role expects these inventory groups:

- `k3s_masters`: Master/control-plane nodes
- `k3s_workers`: Worker/agent nodes
- `os_debian`: Debian/Ubuntu nodes
- `os_redhat`: RHEL/CentOS nodes
- `k3s_cluster`: All K3s nodes (convenience group)

## License

MIT

## Author

sudo-kraken
