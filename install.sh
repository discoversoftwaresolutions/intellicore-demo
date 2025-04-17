#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------------------
# install.sh
# Attempts pip install, then handles ResolutionImpossible for numpy conflicts.
# ------------------------------------------------------------------------------

echo "🔧 Installing Python dependencies..."
if pip install -r requirements.txt; then
  echo "✅ All dependencies installed successfully."
  exit 0
fi

# If we get here, pip failed with ResolutionImpossible
echo
echo "ERROR: ResolutionImpossible: for help visit"
echo "       https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts"
echo
echo "ERROR: Cannot install numpy==1.23.5 and numpy>=1.24"
echo "       because these package versions have conflicting dependencies."
echo
echo "The conflict is caused by:"
echo "  • numpy==1.23.5 (pinned in requirements.txt)"
echo "  • numpy>=1.24    (required by streamlit==1.24.1)"
echo
echo "To resolve this, choose one of the following strategies:"
echo
echo "  1) Downgrade Streamlit to a numpy<1.24–compatible release:"
echo "       pip install streamlit==1.23.1"
echo
echo "  2) Relax or update your numpy pin to >=1.24 (if all other deps allow):"
echo "       sed -i 's/^numpy==1.23.5/numpy>=1.24/' requirements.txt"
echo "       ./install.sh"
echo
echo "  3) Use a constraints file to force compatible versions:"
echo "       echo \"streamlit==1.23.1\" > constraints.txt"
echo "       echo \"numpy==1.23.5\" >> constraints.txt"
echo "       pip install -r requirements.txt -c constraints.txt"
echo
exit 1
