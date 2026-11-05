#!/usr/bin/env bash
# Jules_Setup.sh - Install all necessary tools for building and testing in Jules environment

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Setting up environment for Jules..."

echo "==> Installing build toolchain dependencies..."
"${SCRIPT_DIR}/src/install.sh"

echo "==> Installing testing toolchain dependencies..."
"${SCRIPT_DIR}/test/install.sh"

echo "==> Jules environment setup completed successfully!"
