# Trustable Binary Framework

This project aims to automate the creation of portable, systemd-based projects and generate an SPDX-compliant Software Bill of Materials (SBOM). I need this to complete a proof of concept (POC) for the upcoming presentation on "How to Trust a Binary." The project includes scripts and a structured environment for managing binaries, dependencies, unit files, and metadata, all while ensuring compliance with best practices. Additionally, I have provided a sample C++ project and a service file for this POC. 

This POC is designed to work on aarch64 architectures and has been tested on the Raspberry Pi 4B. It utilizes native compilation directly on the Raspberry Pi and does not support cross-compilation.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Folder Structure](#folder-structure)
3. [Setup](#setup)
4. [How to Use](#how-to-use)
    - [Step 1: Validate Configuration](#step-1-validate-configuration)
    - [Step 2: Compile Source and Populate Portable Structure](#step-2-compile-source-and-populate-portable-structure)
    - [Step 3: Create SquashFS Raw File](#step-3-create-squashfs-raw-file)
    - [Step 4: Generate SPDX SBOM](#step-4-generate-spdx-sbom)
5. [Debugging](#debugging)
6. [Service File Guidelines](#service-file-guidelines)
7. [SPDX SBOM Compliance](#spdx-sbom-compliance)

---

## Prerequisites

Before you begin, ensure the following dependencies are installed:

- Python 3.8 or higher
- `jsonschema` Python package
  ```bash
  pip3 install jsonschema
  ```
- CMake and a compatible C++ compiler
- `squashfs-tools`
  ```bash
  sudo apt-get install squashfs-tools
  ```
- Internet connection (for schema validation and downloads)

---

## Folder Structure

The project directory should follow this structure:

```plaintext
project-root/
├── src/                        # Source files
│   ├── <source_code>.cpp
│   └── CMakeLists.txt
├── config/                     # Configuration files
│   └── portable_config.json
├── build/                      # Build directory (auto-generated)
├── my-portable-service/        # Portable filesystem (auto-populated)
├── output/                     # Output directory for raw file and SBOM
├── scripts/                    # Scripts and schemas
│   ├── compile_and_populate.py
│   ├── create_squashfs.py
│   ├── generate_sbom.py
│   ├── sbom_validation.py
│   ├── validate_config.py
│   ├── portable_env.sh
│   └── data/schemas/
│       ├── portable_config_schema.json
│       └── spdx-schema.json
└── units/                      # Custom unit files (if any)
```

---

## Setup

1. Clone the repository or copy the folder structure to your workspace.
2. Download the SPDX schema for validation:
   ```bash
   wget -O scripts/data/schemas/spdx-schema.json "https://git.yoctoproject.org/poky/plain/meta/lib/oe/spdx.py?h=yocto-4.0.2"
   ```
3. Source the environment script:
   ```bash
   source scripts/portable_env.sh
   ```
   This will set up environment variables and aliases for easier script management.

---

## How to Use

### Step 1: Validate Configuration
Ensure that your `config/portable_config.json` is valid and adheres to the schema.

```bash
validate_config
```
If successful, the script will output:
```plaintext
Validation passed!
```

### Step 2: Compile Source and Populate Portable Structure
Compile your source code and populate the `my-portable-service/` directory with the necessary binaries and dependencies.

```bash
compile_and_populate
```
This step:
- Builds the source code from `src/`.
- Copies the binaries to `my-portable-service/usr/bin/`.
- Copies dependencies to `my-portable-service/lib/aarch64-linux-gnu/`.
- Copies unit files to `my-portable-service/etc/systemd/system/`.

### Step 3: Create SquashFS Raw File
Package the portable structure into a SquashFS raw file.

```bash
create_raw
```
The raw file will be saved in the `output/` directory with the name format `<portable_name>-<version>.raw`.

### Step 4: Generate SPDX SBOM
Generate the SBOM for the portable project to comply with SPDX standards.

```bash
generate_sbom
```
The SBOM file will be saved in the `output/` directory with the name format `<portable_name>-<version>-sbom.json`.

---

## Debugging

### 1. Fixing Port Binding Issues
If your service fails with the error `bind: Address already in use`, it means the port your application is trying to bind to is already in use. To resolve this:

1. Check the port currently in use:
   ```bash
   sudo netstat -tuln | grep <port_number>
   ```
2. Stop the process using the port:
   ```bash
   sudo fuser -k <port_number>/tcp
   ```
3. Restart your service:
   ```bash
   systemctl restart <service_name>
   ```

### 2. Relax Unit File Restrictions
Update the unit file (e.g., `key-value-server-1.0.0.service`) to disable some namespace features that might be causing issues:

Add these lines to the `[Service]` section of your unit file:

```ini
[Service]
...
ProtectSystem=no
ProtectHome=no
PrivateTmp=no
ReadWritePaths=/etc /var /tmp /run /proc /sys
```

After making these changes, re-run the `compile_and_populate` script to ensure the updated unit file is included in the portable image.

---

## Service File Guidelines

### Naming Convention
The service file must include the portable name and version. For example, if your portable is named `key-value-server` with version `1.0.0`, the service file should be named `key-value-server-1.0.0.service`.

### Template Service File
Below is a template for a systemd service file:

```ini
[Unit]
Description=<Description of your service>
After=network.target

[Service]
ExecStart=/usr/bin/<binary_name>
StandardOutput=journal

# Namespace and filesystem settings
ProtectSystem=no
ProtectHome=no
PrivateTmp=no
ReadWritePaths=/etc /var /tmp /run /proc /sys

[Install]
WantedBy=multi-user.target
```

### Required Fields
1. **[Unit] Section:**
   - `Description`: Provide a meaningful description of your service.
   - `After`: Specify dependencies for startup order (e.g., `network.target`).

2. **[Service] Section:**
   - `ExecStart`: Specify the binary to run (e.g., `/usr/bin/<binary_name>`).
   - `ProtectSystem`, `ProtectHome`, `PrivateTmp`: Set these to `no` if additional access is needed.
   - `ReadWritePaths`: List paths that should be writable during service execution.

3. **[Install] Section:**
   - `WantedBy`: Define the target for service installation (e.g., `multi-user.target`).

Replace placeholders (e.g., `<Description of your service>` and `<binary_name>`) with appropriate values for your project.

---

## SPDX SBOM Compliance

The SBOM generated adheres to SPDX 2.3 standards and includes:

- Metadata about the portable binary and dependencies.
- Licenses and relationships between components.
- SHA-1 hash for file verification.

To validate the SBOM:

```bash
python3 scripts/sbom_validation.py
```