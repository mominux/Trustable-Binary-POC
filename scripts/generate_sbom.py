import os
import json
import hashlib
from datetime import datetime
from jsonschema import validate, ValidationError

# Paths
ROOT_DIR = os.environ.get("PORTABLE_PROJECT_ROOT", os.getcwd())
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
SCHEMA_PATH = os.path.join(ROOT_DIR, "scripts/data/schemas/spdx-schema.json")
CONFIG_PATH = os.path.join(ROOT_DIR, "config/portable_config.json")

# License map for dependencies
LICENSE_MAP = {
    "libspdlog.so.1": "MIT",
    "libfmt.so.8": "MIT",
    "libstdc++.so.6": "GPLv3",
    "libgcc_s.so.1": "GPLv3",
    "libc.so.6": "LGPLv2.1",
    "libm.so.6": "LGPLv2.1",
}

# Helper to calculate SHA-1 hash
def calculate_hash(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()

# Generate SPDX SBOM
def generate_sbom():
    print("Generating SPDX SBOM...")

    # Load portable_config.json
    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)

    portable_name = config["name"]
    portable_version = config["version"]

    # SPDX document metadata
    sbom = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "documentNamespace": f"http://spdx.org/spdxdocs/{portable_name}-{portable_version}-{datetime.utcnow().isoformat()}",
        "name": portable_name,
        "creationInfo": {
            "created": datetime.utcnow().isoformat(),
            "creators": ["Tool: SPDX Generator Script"],
            "licenseListVersion": "3.18"
        },
        "packages": [],
        "files": [],
        "relationships": [],
    }

    # Process the binary and dependencies
    service_dir = os.path.join(ROOT_DIR, "my-portable-service")
    binary_path = os.path.join(service_dir, "usr/bin", portable_name)
    lib_dir = os.path.join(service_dir, "lib/aarch64-linux-gnu")

    # Add main binary
    sbom["packages"].append({
        "SPDXID": f"SPDXRef-Package-{portable_name}",
        "name": portable_name,
        "versionInfo": portable_version,
        "licenseDeclared": "MIT",
        "downloadLocation": "NOASSERTION",
        "filesAnalyzed": True,
        "packageVerificationCode": {
            "packageVerificationCodeValue": calculate_hash(binary_path)
        },
        "licenseConcluded": "MIT",
        "licenseInfoFromFiles": ["MIT"],
    })

    # Add dependencies
    for lib_file in os.listdir(lib_dir):
        lib_path = os.path.join(lib_dir, lib_file)
        license = LICENSE_MAP.get(lib_file, "UNKNOWN")
        lib_spdx_id = f"SPDXRef-Package-{lib_file}"

        # Add dependency package
        sbom["packages"].append({
            "SPDXID": lib_spdx_id,
            "name": lib_file,
            "versionInfo": "N/A",
            "licenseDeclared": license,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": True,
            "packageVerificationCode": {
                "packageVerificationCodeValue": calculate_hash(lib_path)
            },
            "licenseConcluded": license,
            "licenseInfoFromFiles": [license],
        })

        # Add relationship
        sbom["relationships"].append({
            "spdxElementId": f"SPDXRef-Package-{portable_name}",
            "relatedSpdxElement": lib_spdx_id,
            "relationshipType": "DEPENDS_ON"
        })

    # Write the SBOM
    sbom_file = os.path.join(OUTPUT_DIR, f"{portable_name}-{portable_version}-sbom.json")
    with open(sbom_file, "w") as f:
        json.dump(sbom, f, indent=4)
    print(f"SPDX SBOM generated: {sbom_file}")

    # Validate SBOM
    validate_sbom(sbom_file)

# Validate SPDX SBOM
def validate_sbom(sbom_file):
    print("Validating SPDX SBOM...")
    # Load SBOM
    with open(sbom_file, "r") as f:
        sbom = json.load(f)
    # Load SPDX schema
    with open(SCHEMA_PATH, "r") as f:
        schema = json.load(f)

    # Validate
    try:
        validate(instance=sbom, schema=schema)
        print("SPDX SBOM validation successful!")
    except ValidationError as e:
        print("SPDX SBOM validation failed!")
        print(f"Error: {e.message}")

if __name__ == "__main__":
    generate_sbom()

