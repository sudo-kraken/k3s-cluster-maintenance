# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-07-02

### 🚀 Major Refactor: Native Kubernetes Modules

**BREAKING CHANGE**: Refactored from shell commands to proper Ansible Kubernetes modules for better reliability, error handling, and maintainability.

### ✨ Added
- **Native Kubernetes Operations** - Complete migration to `kubernetes.core` collection
- **Custom Drain Logic** - Native pod deletion with DaemonSet filtering instead of kubectl drain
- **Cross-Platform Compatibility** - No longer requires shell-specific tools
- **Collections Requirements** - Added `collections/requirements.yml` for dependency management
- **Installation Script** - Automated collection installation with `install-collections.sh`
- **Longhorn Volume Health Checks** - Added validation for degraded and faulted volumes before maintenance
- **Longhorn Volume Recovery** - Automatic wait and recovery mechanism for degraded volumes
- **Storage Safety Features** - Pre-maintenance validation prevents unsafe operations on unhealthy storage

### 🔧 Changed
- **Prerequisites** - Now requires `kubernetes.core` collection and Python Kubernetes client
- **Node Operations** - All Kubernetes operations now use native modules instead of shell commands
- **Readiness Checks** - Node Ready status monitoring uses `k8s_info` with wait conditions
- **Drain Operations** - Custom drain logic using native pod deletion instead of kubectl drain
- **Output Display** - Cleaner, more concise progress messages throughout maintenance workflow

### 🐛 Fixed
- **Resume Functionality** - Resume task now only runs when explicitly called with `--tags resume`
- **Shell Dependencies** - Eliminated dependency on bash-specific commands and JSON parsing tools
- **Platform Limitations** - Better Windows and cross-platform support
- **Error Display** - Fixed drain operations showing red errors for normal timeout conditions
- **Terminal Compatibility** - Improved display across different terminal environments
- **Variable References** - Fixed undefined variable issues in pod filtering logic
- **Longhorn Volume Safety** - Prevents maintenance on nodes with degraded storage volumes

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
