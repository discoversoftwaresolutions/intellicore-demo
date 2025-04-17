#!/usr/bin/env bash
set -euo pipefail

#-------------------------------------------------------------------------------
# Script: setup_env.sh
# Purpose: Create a Python 3.10 virtual environment and install dependencies
# Usage: ./setup_env.sh
#-------------------------------------------------------------------------------

# 1. Ensure Python 3.10 is available
PYTHON_BIN=python3.10
if ! command -v "${PYTHON_BIN}" &> /dev/null; then
  echo "Error: ${PYTHON_BIN} not found. Please install Python 3.10 and try again."
  exit 1
fi

# 2. Define environment directory
ENV_DIR="dss-env"

# 3. Create the virtual environment
echo "Creating virtual environment in ./${ENV_DIR} using ${PYTHON_BIN}..."
"${PYTHON_BIN}" -m venv "${ENV_DIR}"

# 4. Activate the virtual environment
#    For POSIX shells (bash, zsh, etc.)
source "${ENV_DIR}/bin/activate"

# 5. Upgrade tooling
echo "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

# 6. Install core dependencies
echo "Installing numpy..."
pip install numpy

# 7. Attempt alibi-detect>=1.9, fallback if unavailable
echo "Attempting to install alibi-detect>=1.9..."
if pip install "alibi-detect>=1.9"; then
  echo "✅ Successfully installed alibi-detect>=1.9"
else
  echo "⚠️ alibi-detect>=1.9 not found on PyPI. Installing latest 0.x instead..."
  pip install "alibi-detect>=0.12.0,<1.0.0"
  echo "✅ Installed alibi-detect 0.x series"
fi

echo
echo "🎉 Environment setup complete!"
echo "   • Activate it with:  source ./${ENV_DIR}/bin/activate"
echo "   • Deactivate with:     deactivate"
your-project/setup_env.sh
