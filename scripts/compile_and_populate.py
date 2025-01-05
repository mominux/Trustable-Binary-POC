import os
import subprocess
import shutil

# Get environment variables
PROJECT_ROOT = os.environ.get("PORTABLE_PROJECT_ROOT")
BUILD_DIR = os.environ.get("PORTABLE_BUILD_DIR")
SERVICE_DIR = os.environ.get("PORTABLE_SERVICE_DIR")
OUTPUT_DIR = os.environ.get("PORTABLE_OUTPUT_DIR")

if not PROJECT_ROOT or not BUILD_DIR or not SERVICE_DIR or not OUTPUT_DIR:
    raise EnvironmentError("Environment not set. Please source 'portable_env.sh'.")

# Define necessary portable directory structure
PORTABLE_STRUCTURE = [
    "bin",
    "dev",
    "etc",
    "etc/systemd/system",
    "lib/aarch64-linux-gnu",
    "proc",
    "run",
    "sys",
    "tmp",
    "usr/bin",
    "var/tmp"
]

def create_portable_structure():
    """Create the required directory structure for the portable service."""
    print("Creating portable directory structure...")
    for subdir in PORTABLE_STRUCTURE:
        path = os.path.join(SERVICE_DIR, subdir)
        os.makedirs(path, exist_ok=True)

    # Create symlink for bin -> usr/bin
    bin_link = os.path.join(SERVICE_DIR, "bin")
    usr_bin_dir = os.path.join(SERVICE_DIR, "usr", "bin")
    if os.path.islink(bin_link):
        # Remove existing symlink if it's incorrect
        if os.readlink(bin_link) != usr_bin_dir:
            os.unlink(bin_link)
    elif os.path.exists(bin_link):
        # Remove existing directory if it conflicts
        shutil.rmtree(bin_link)

    # Create symlink if it doesn't exist
    if not os.path.exists(bin_link):
        os.symlink(usr_bin_dir, bin_link)
    print("Portable directory structure created.")


def compile_source():
    """Compile the source code."""
    print("Compiling source code...")
    src_dir = os.path.join(PROJECT_ROOT, "src")
    cmake_file = os.path.join(src_dir, "CMakeLists.txt")
    binary_name = "key-value-server"  # Adjust for your project
    binary_path = os.path.join(BUILD_DIR, binary_name)

    # Run CMake commands
    subprocess.run(["cmake", src_dir, "-B", BUILD_DIR], check=True)
    subprocess.run(["cmake", "--build", BUILD_DIR], check=True)

    # Copy binary to portable directory
    usr_bin_dir = os.path.join(SERVICE_DIR, "usr", "bin")
    shutil.copy2(binary_path, os.path.join(usr_bin_dir, binary_name))
    print(f"Binary compiled and copied to: {os.path.join(usr_bin_dir, binary_name)}")

def populate_essential_files():
    """Populate essential files like os-release and service files."""
    print("Populating essential files...")
    
    # Copy os-release
    os_release_content = """NAME="Key-Value Server Portable"
VERSION="1.0.0"
"""
    with open(os.path.join(SERVICE_DIR, "etc", "os-release"), "w") as f:
        f.write(os_release_content)

    # Create machine-id
    machine_id_path = os.path.join(SERVICE_DIR, "etc", "machine-id")
    if not os.path.exists(machine_id_path):
        with open(machine_id_path, "w") as f:
            f.write("")

    # Copy service files from units/
    units_dir = os.path.join(PROJECT_ROOT, "units")
    systemd_dir = os.path.join(SERVICE_DIR, "etc", "systemd", "system")
    if os.path.exists(units_dir):
        for unit_file in os.listdir(units_dir):
            shutil.copy2(os.path.join(units_dir, unit_file), os.path.join(systemd_dir, unit_file))
    
    # Create resolv.conf
    resolv_conf_path = os.path.join(SERVICE_DIR, "etc", "resolv.conf")
    if not os.path.exists(resolv_conf_path):
        with open(resolv_conf_path, "w") as f:
            f.write("")

    print("Essential files populated.")

def copy_libraries():
    """Copy the required shared libraries into the portable structure."""
    print("Copying required shared libraries...")
    usr_bin_dir = os.path.join(SERVICE_DIR, "usr", "bin")
    lib_dir = os.path.join(SERVICE_DIR, "lib", "aarch64-linux-gnu")

    binary_path = os.path.join(usr_bin_dir, "key-value-server")
    ld_linux_path = "/lib/ld-linux-aarch64.so.1"

    # Use ldd to find and copy libraries
    ldd_output = subprocess.check_output(["ldd", binary_path]).decode().strip()
    for line in ldd_output.split("\n"):
        parts = line.split("=>")
        if len(parts) == 2:
            lib_path = parts[1].strip().split(" ")[0]
            if os.path.exists(lib_path):
                shutil.copy2(lib_path, lib_dir)

    # Copy ld-linux-aarch64.so.1 manually
    shutil.copy2(ld_linux_path, os.path.join(SERVICE_DIR, "lib"))
    print("Required libraries copied.")

def main():
    """Main function to orchestrate the compilation and population."""
    create_portable_structure()
    compile_source()
    populate_essential_files()
    copy_libraries()
    print("Portable structure populated successfully!")

if __name__ == "__main__":
    main()

