#!/bin/bash

# Determine the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Project Root Directory (parent of the script directory)
export PORTABLE_PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Set paths relative to the project root
export PORTABLE_SCRIPTS_DIR="$PORTABLE_PROJECT_ROOT/scripts"
export PORTABLE_CONFIG_DIR="$PORTABLE_PROJECT_ROOT/config"
export PORTABLE_BUILD_DIR="$PORTABLE_PROJECT_ROOT/build"
export PORTABLE_SERVICE_DIR="$PORTABLE_PROJECT_ROOT/my-portable-service"
export PORTABLE_OUTPUT_DIR="$PORTABLE_PROJECT_ROOT/output"

# Python Aliases
alias validate_config="python3 $PORTABLE_SCRIPTS_DIR/validate_config.py"
alias compile_and_populate="python3 $PORTABLE_SCRIPTS_DIR/compile_and_populate.py"
alias generate_sbom="python3 $PORTABLE_SCRIPTS_DIR/generate_sbom.py"
alias create_raw="python3 $PORTABLE_SCRIPTS_DIR/create_squashfs.py"
alias generate_sbom="python3 $PORTABLE_SCRIPTS_DIR/generate_sbom.py"

# Status Messages
echo "Portable project environment loaded."
echo "  - Root directory: $PORTABLE_PROJECT_ROOT"
echo "  - Scripts directory: $PORTABLE_SCRIPTS_DIR"
echo "  - Config directory: $PORTABLE_CONFIG_DIR"
echo "  - Build directory: $PORTABLE_BUILD_DIR"
echo "  - Service directory: $PORTABLE_SERVICE_DIR"
echo "  - Output directory: $PORTABLE_OUTPUT_DIR"
echo ""
echo "Available Commands: "
echo "  1 - validate_config: Validate the configuration against schema."
echo "  2 - compile_and_populate: Compile source code and populate portable structure."
echo "  3 - generate_sbom: Generate the SPDX software bill of materials (SBOM) for the portable project."
echo "  4 - create_raw: create the raw file"