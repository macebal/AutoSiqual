#!/bin/bash

# Update the version in poetry
poetry version "${version_bump_type}"

# Get the new version from pyproject.toml
new_version=$(poetry version --short)

# Update the __version__ in src/__init__.py
init_py="src/__init__.py"

if [ -f "$init_py" ]; then
    sed -i 's/__version__ = .*/__version__ = "'$new_version'"/' "$init_py"
    echo "Updated version in $init_py to $new_version"
else
    echo "Error: $init_py not found."
fi