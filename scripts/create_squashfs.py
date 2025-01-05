import os
import subprocess

# Get environment variables
SERVICE_DIR = os.environ.get("PORTABLE_SERVICE_DIR")
OUTPUT_DIR = os.environ.get("PORTABLE_OUTPUT_DIR")
CONFIG_DIR = os.environ.get("PORTABLE_CONFIG_DIR")

if not SERVICE_DIR or not OUTPUT_DIR or not CONFIG_DIR:
    raise EnvironmentError("Environment not set. Please source 'portable_env.sh'.")

# Load portable configuration
import json
config_path = os.path.join(CONFIG_DIR, "portable_config.json")
if not os.path.exists(config_path):
    raise FileNotFoundError(f"Configuration file not found: {config_path}")

with open(config_path, "r") as f:
    config = json.load(f)

# Validate mandatory fields in config
if "name" not in config or "version" not in config:
    raise ValueError("Configuration must include 'name' and 'version' fields.")

# Define the output filename
image_name = f"{config['name']}-{config['version']}.raw"
image_path = os.path.join(OUTPUT_DIR, image_name)

def create_squashfs_image():
    """Create the SquashFS image."""
    if not os.path.exists(SERVICE_DIR):
        raise FileNotFoundError(f"Service directory not found: {SERVICE_DIR}")

    print(f"Creating SquashFS image: {image_path}")
    subprocess.run(["mksquashfs", SERVICE_DIR, image_path, "-comp", "xz"], check=True)
    print(f"SquashFS image created successfully: {image_path}")

def main():
    create_squashfs_image()

if __name__ == "__main__":
    main()
