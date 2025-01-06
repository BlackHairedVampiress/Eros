import os
import zipfile
import shutil


# Function to create a CBZ file from a directory
def _create_cbz_from_directory(dir_path, cbz_filename):
    cbz_filepath = os.path.join(os.getcwd(), cbz_filename)

    # Prepare a zip file with the .cbz extension
    with zipfile.ZipFile(cbz_filepath, "w", zipfile.ZIP_DEFLATED) as cbz:
        # Walk through the directory and add only the files to the CBZ (no subdirectories)
        for root, _, files in os.walk(dir_path):
            # Only add files that are directly inside this directory, not in subdirectories
            if root == dir_path:
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add file to the zip, preserving its path relative to the directory
                    arcname = os.path.relpath(file_path, dir_path)
                    cbz.write(file_path, arcname)

    print(f"Created {cbz_filepath}")


# Function to delete a directory and its contents
def delete_directory(dir_path):
    try:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"Deleted directory {dir_path}")
        else:
            print(f"Directory {dir_path} does not exist, skipping deletion.")
    except Exception as e:
        print(f"Failed to delete {dir_path}: {e}")


# Function to process each directory in the current working directory
def process_directories():
    # Get the current working directory
    current_dir = os.getcwd()

    # Loop through each directory in the current working directory
    for entry in os.scandir(current_dir):
        if entry.is_dir():  # Check if it's a directory
            dir_name = entry.name
            dir_path = entry.path

            # Create a CBZ for the directory itself (including its direct contents only)
            _create_cbz_from_directory(dir_path, f"{dir_name}.cbz")

            # Now process any subdirectories within the current directory
            try:
                for sub_entry in os.scandir(dir_path):
                    if (
                        sub_entry.is_dir()
                    ):  # If it's a subdirectory, create a CBZ for it
                        subdir_name = sub_entry.name
                        subdir_path = sub_entry.path
                        # Include both parent directory name and subdirectory name in the CBZ filename
                        subdir_cbz_filename = f"{dir_name} - {subdir_name}.cbz"

                        # Create a CBZ for the subdirectory (including only the files in that subdirectory)
                        _create_cbz_from_directory(subdir_path, subdir_cbz_filename)
            except PermissionError as pe:
                print(
                    f"Permission denied while accessing subdirectories in {dir_path}: {pe}"
                )
            except Exception as e:
                print(f"Error while processing subdirectories in {dir_path}: {e}")

            # After creating the CBZ for the directory and its subdirectories, delete the directory
            delete_directory(dir_path)
