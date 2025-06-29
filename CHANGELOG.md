# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-29

### Initial Release

Enterprise-grade K3s cluster OS maintenance automation tool with modular role-based architecture for safely applying operating system updates to nodes with comprehensive health checks and storage protection.

### 🏢 Enterprise Architecture
- **Modular Ansible Role Structure** - Professional role-based architecture in `roles/k3s_node_maintenance/`
- **Task Separation** - 8 logical task files for maintainability (prerequisites, package checks, cluster prep, updates, etc.)
- **Group Variables** - Node type and OS-specific configuration via `group_vars/`
- **Default Variables** - Centralised configuration management with sensible defaults
- **Galaxy-Ready Role** - Proper metadata and structure for Ansible Galaxy distribution
- **CI/CD Integration** - GitHub Actions workflow for automated testing and validation

### 🎯 Smart Maintenance Logic
- **Early Package Detection** - Checks for available updates BEFORE cordoning/draining nodes
- **Prevents Unnecessary Operations** - Tool exits gracefully if no packages need updating
- **DRY Implementation** - Uses `reboot_required` fact to eliminate code duplication
- **Smart Exit Logic** - Avoids disruption of healthy, up-to-date nodes
- **Prerequisite Validation** - Validates required binaries before starting operations

### 🔧 Zero-Downtime OS Updates
- **Sequential Node Processing** - Updates only one node at a time for cluster stability
- **Health Monitoring** - Comprehensive pre/post-update validation of cluster and storage
- **Master Node Safety** - Specialised control plane handling with quorum protection
- **Block/Rescue Structure** - Proper fallback handling for drain operations
- **Reboot Coordination** - Intelligent reboot management with cluster awareness

### 📦 Multi-OS Package Management
- **APT Integration** - Complete Ubuntu/Debian support with module-based operations
- **DNF Integration** - Full RHEL/CentOS/AlmaLinux support with change tracking
- **Package Reporting** - Clean summaries showing upgrade counts and key packages
- **Reboot Detection** - Intelligent detection with fallbacks for various distributions
- **Security Updates** - Automated application of critical security patches

### 🛠️ Professional Tools
- **Role-Based Playbooks** - Clean `maintenance.yml` using enterprise role structure
- **Group Variables** - Separate configuration for masters/workers and OS families
- **Shell Integration** - Streamlined commands (`k3s-maintain-workers`, `k3s-maintain-cluster`)
- **Debug Support** - Comprehensive debugging and troubleshooting capabilities
- **Emergency Recovery** - Built-in tools for handling stuck operations

### 🔌 Storage & Infrastructure
- **Longhorn Integration** - Native support for Longhorn storage health monitoring
- **Volume Validation** - Pre/post-maintenance storage health verification
- **Node Scheduling** - Proper scheduling control during maintenance operations
- **Inventory Management** - Group-based inventory with OS and role classifications

### 💻 Developer Experience
- **Modern Inventory Structure** - Group-based organisation (`k3s_masters`, `k3s_workers`, `os_debian`, `os_redhat`)
- **Ansible Configuration** - Proper `ansible.cfg` with optimised settings
- **Requirements Management** - Python dependencies file for development environments
- **Quality Assurance** - Ansible lint, YAML validation, and shell syntax checks
- **Documentation** - Comprehensive role documentation and usage examples

### 📚 Documentation & Setup
- **Architecture Documentation** - Detailed explanation of role structure and benefits
- **Installation Guide** - Multi-OS installation instructions with automated setup
- **Usage Examples** - Real-world scenarios and command references
- **Troubleshooting** - Extensive guide covering common issues and solutions
- **Shell Compatibility** - Full bash/zsh support with auto-detection

### 🔒 Security & Quality
- **Enhanced .gitignore** - Role-specific patterns and sensitive file protection
- **CI/CD Pipeline** - Automated testing with GitHub Actions
- **No Legacy Cruft** - Clean, modern command structure without deprecated aliases
- **SSH Security** - Proper key management and connection configuration

### 📄 License
- MIT License for open source distribution
