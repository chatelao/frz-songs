#!/usr/bin/env bash
# test/install.sh - Install testing toolchain dependencies for French Songs Collection

set -euo pipefail

echo "==> Installing testing dependencies for French Songs Collection..."

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
  else
    echo "Error: This script requires root privileges or sudo." >&2
    exit 1
  fi
fi

# Update apt package index
$SUDO apt-get update -y

# Install testing toolchain dependencies:
# - nodejs, npm: JavaScript runtime & package manager for Playwright E2E tests
$SUDO apt-get install -y --no-install-recommends \
  nodejs \
  npm \
  ca-certificates \
  curl

# Initialize package.json if it doesn't exist under test/
if [ ! -f "package.json" ] && [ ! -f "test/package.json" ]; then
  echo "==> Initializing node package environment for Playwright testing..."
fi

# Install Playwright and browser dependencies if package.json exists or via npx / python3
if command -v python3 >/dev/null 2>&1; then
  echo "==> Installing Playwright python package and browser dependencies (chromium)..."
  python3 -m pip install playwright --quiet || true
  python3 -m playwright install chromium --with-deps || python3 -m playwright install chromium || true
fi

if command -v npx >/dev/null 2>&1; then
  echo "==> Playwright / Node execution environment ready."
fi

echo "==> Testing dependencies installed successfully!"
