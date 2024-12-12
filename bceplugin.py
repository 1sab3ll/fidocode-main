import zipfile
import os
from tkinter import filedialog, messagebox, Tk

def convert_zip_to_bceplugin():
    # Open a file dialog to select a .zip file
    zip_file_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
    
    if not zip_file_path:
        return  # User cancelled the dialog
    
    try:
        # Define the path for the new .bceplugin file
        bceplugin_file_path = zip_file_path.replace(".zip", ".bceplugin")
        
        # Open the ZIP file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Create the new .bceplugin file (it's essentially the zip file with a different extension)
            with open(bceplugin_file_path, 'wb') as bceplugin_file:
                for file_info in zip_ref.infolist():
                    # Extract all files from the zip into the .bceplugin file
                    zip_ref.extract(file_info, bceplugin_file.name)
        
        # Show success message
        messagebox.showinfo("Success", f"ZIP file successfully converted to {bceplugin_file_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert ZIP file: {e}")

if __name__ == "__main__":
    # Initialize tkinter window (needed for file dialogs and message boxes)
    root = Tk()
    root.withdraw()  # Hide the root window
    
    convert_zip_to_bceplugin()  # Convert the selected ZIP to .bceplugin file
