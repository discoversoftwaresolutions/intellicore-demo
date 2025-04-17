#!/usr/bin/env bash
set -euo pipefail

# 1. System prerequisites (Ubuntu)
sudo apt update
sudo apt install -y \
  build-essential \
  python3.10-venv python3.10-dev \
  portaudio19-dev

# 2. Create & activate Python 3.10 venv
PYTHON_BIN=python3.10
ENV_DIR="venv"
"$PYTHON_BIN" -m venv "$ENV_DIR"
# shellcheck disable=SC1091
source "${ENV_DIR}/bin/activate"

# 3. Upgrade pip and friends
pip install --upgrade pip setuptools wheel

# 4. Install Python dependencies
pip install -r requirements.txt

echo
echo "✅ Environment ready!"
echo "   • Activate with:  source ${ENV_DIR}/bin/activate"
echo "   • Run demo:      streamlit run dashboard.py"
