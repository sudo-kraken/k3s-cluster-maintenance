# K3s Node Maintenance Role

This role provides automated OS patching and maintenance for K3s cluster nodes with zero-downtime operations.

## Role Variables

### Default Variables (`defaults/main.yml`)
- `k3s_node_maintenance_wait_timeout`: Maximum time to wait for drain operations (default: 600s)
- `k3s_node_maintenance_drain_timeout`: Timeout for node draining (default: 300s)
- `k3s_node_maintenance_drain_grace_period`: Grace period for pod termination (default: 30s)
- `k3s_node_maintenance_reboot_pause`: Initial pause after reboot initiation (default: 30s)
- `k3s_node_maintenance_apt_cache_valid_time`: APT cache validity time (default: 3600s)
- `k3s_node_maintenance_node_type`: Node type - "master" or "worker" (default: "worker")
- `k3s_node_maintenance_critical_node`: Whether node is critical (default: false)
- `k3s_node_maintenance_longhorn_enabled`: Enable Longhorn checks (default: true)

**Note**: Reboot handling uses adaptive monitoring without timeouts, waiting for actual node state changes.

### Group Variables

#### `group_vars/k3s_masters/main.yml`
- Extended timeouts for master nodes
- Critical node handling enabled
- Conservative reboot behaviour

#### `group_vars/k3s_workers/main.yml`
- Standard timeouts for worker nodes
- Non-critical node handling
- Standard reboot behaviour

#### `group_vars/os_debian/main.yml`
- APT package manager configuration
- Debian-specific settings

#### `group_vars/os_redhat/main.yml`
- DNF package manager configuration
- RedHat-specific settings

## Task Structure

The role is organised into logical task files:

- `tasks/main.yml`: Main orchestration
- `tasks/prerequisites.yml`: Pre-flight checks
- `tasks/package_checks.yml`: Update detection and early exit
- `tasks/cluster_preparation.yml`: Node cordoning and draining
- `tasks/package_updates.yml`: OS-specific update inclusion
- `tasks/debian_updates.yml`: Debian/Ubuntu package updates
- `tasks/redhat_updates.yml`: RHEL/CentOS package updates
- `tasks/reboot_handling.yml`: Smart reboot coordination with adaptive monitoring
- `tasks/cluster_restoration.yml`: Node restoration
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
- `longhorn`: Longhorn-specific operations

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
ansible-playbook -i hosts.yml maintenance.yml --tags resume
```

## Dependencies

None. This is a standalone role.

## Example Playbook

```yaml
---
- name: K3s Cluster Node Maintenance
  hosts: "{{ target | default('k3s_cluster') }}"
  gather_facts: false
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
