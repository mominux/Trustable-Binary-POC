import json
import os
import jsonschema
from jsonschema import validate

def load_and_validate_config(config_path, schema_path):
    """Load and validate JSON configuration against schema."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(config_path, 'r') as f:
        config = json.load(f)
    with open(schema_path, 'r') as f:
        schema = json.load(f)

    # Validate JSON
    try:
        validate(instance=config, schema=schema)
        print("Configuration is valid.")
    except jsonschema.exceptions.ValidationError as e:
        print(f"Validation Error: {e.message}")
        raise

    return config

if __name__ == "__main__":
    # Adjust paths to match the current folder structure
    config_path = "config/portable_config.json"
    schema_path = "scripts/data/schemas/portable_config_schema.json"
    config = load_and_validate_config(config_path, schema_path)
