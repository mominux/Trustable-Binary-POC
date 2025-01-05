import json
from jsonschema import validate, ValidationError

# Paths
sbom_path = "output/key-value-server-1.0.0-sbom.json"
schema_path = "data/schema/spdx-schema.json"

# Load files
with open(sbom_path, "r") as f:
    sbom = json.load(f)

with open(schema_path, "r") as f:
    schema = json.load(f)

# Validate
try:
    validate(instance=sbom, schema=schema)
    print("SPDX SBOM is valid!")
except ValidationError as e:
    print("SPDX SBOM validation failed!")
    print(e.message)

