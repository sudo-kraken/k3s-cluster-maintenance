#!/bin/bash
# Install required Ansible collections for K3s maintenance

echo "🔧 Installing Ansible collections for K3s cluster maintenance..."

# Install kubernetes.core collection
if ! ansible-galaxy collection list | grep -q kubernetes.core; then
    echo "📦 Installing kubernetes.core collection..."
    ansible-galaxy collection install kubernetes.core
else
    echo "✅ kubernetes.core collection already installed"
fi

# Check if requirements file exists and install from it
if [ -f "collections/requirements.yml" ]; then
    echo "📦 Installing collections from requirements.yml..."
    ansible-galaxy collection install -r collections/requirements.yml
fi

echo "🔍 Verifying installations..."
ansible-galaxy collection list | grep -E "(kubernetes\.core|community\.general)"

echo "✅ Collection installation complete!"
echo ""
echo "📋 Python dependencies (install with pip install -r requirements.txt):"
echo "   - kubernetes>=33.1.0"
echo "   - PyYAML>=6.0"
echo ""
echo "🚀 Ready to run K3s maintenance with native Kubernetes modules!"
