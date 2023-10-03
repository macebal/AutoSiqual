#!/bin/bash

set -x 
# Find the path to the current Python environment's site-packages directory
PYTHON_EXECUTABLE="$(command -v python)"
PYTHON_LIB_FOLDER="$(dirname "$($PYTHON_EXECUTABLE -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')")"

# Construct the designer tool path based on the operating system
DESIGNER_PATH="$PYTHON_LIB_FOLDER/site-packages/qt5_applications/Qt/bin/designer"

# Check if the designer tool exists
if [ -f "$DESIGNER_PATH" ]; then
    # Execute the designer tool
    "$DESIGNER_PATH"
else
    echo "Designer tool not found for the current Python environment."
    exit 1
fi
