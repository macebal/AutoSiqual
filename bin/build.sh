#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

#Delete previous files
rm -r dist/

#Run pyinstaller to create the executables in the dist/folder
pyinstaller src/main.py --onefile --noconsole

#copy the config.json file and the img/ folder to the dist folder
cp config.json dist/config.json
cp -fR img/ dist/

# #rename main.exe to AutoSiqual vX.X.X
new_filename="AutoSiqual v$(poetry version -s)"
if [ -f "dist/main.exe" ]; then
    # Rename 'main.exe' to the new filename
    mv "dist/main.exe" "dist/$new_filename.exe"
    echo -e "${YELLOW}Renamed main.exe to $new_filename.exe${NC}"
else
    echo -e "${RED}Error: dist/main.exe not found.${NC}"
fi

# Zip everything in 'dist/' directory into 'new_filename.zip'
# On windows, requires installation of zip to automate this step. See:
# https://stackoverflow.com/questions/38782928/how-to-add-man-and-zip-to-git-bash-installation-on-windows
if [ -d "dist" ]; then
    (cd "dist" && zip -r "${new_filename}.zip" ./*)
    echo -e "${YELLOW}Zipped 'dist/' contents into '${new_filename}.zip'${NC}"
else
    echo "Error: 'dist/' directory not found."
    exit 1
fi

echo -e "${GREEN}dist/${new_filename}.zip is ready to distribute. If the zip didn't get built, see bin/build.sh${NC}"