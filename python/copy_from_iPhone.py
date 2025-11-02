import os
import shutil
import sys
from datetime import datetime

def copy_files(source_folder, destination_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.mov', '.heic')):
                source_path = os.path.join(root, file)
                source_size = os.path.getsize(source_path)
                source_mtime = os.path.getmtime(source_path)

                modification_time = datetime.fromtimestamp(source_mtime)
                destination_subfolder = os.path.join(destination_folder, modification_time.strftime('%Y-%m'))
                os.makedirs(destination_subfolder, exist_ok=True)

                destination_path = os.path.join(destination_subfolder, file)
                counter = 1
                while os.path.exists(destination_path):
                    destination_size = os.path.getsize(destination_path)
                    destination_mtime = os.path.getmtime(destination_path)

                    if source_size == destination_size and source_mtime == destination_mtime:
                        print(f"Skipping {source_path} - file already exists in destination folder")
                        break

                    file_name, file_extension = os.path.splitext(file)
                    destination_path = os.path.join(destination_subfolder, f"{file_name}_{counter:02d}{file_extension}")
                    counter += 1
                else:
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied {source_path} to {destination_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <source_folder> <destination_folder>")
        sys.exit(1)

    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]

    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        sys.exit(1)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Created destination folder '{destination_folder}'.")

    copy_files(source_folder, destination_folder)
