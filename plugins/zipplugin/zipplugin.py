import zipfile
import os

def create_test_plugin():
    # The folder containing the plugin
    folder_name = 'test_plugin'
    # Create the zip file
    with zipfile.ZipFile(f"{folder_name}.bceplugin", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_name):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_name))
    print(f"Created {folder_name}.bceplugin successfully!")

create_test_plugin()
