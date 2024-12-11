import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

def convert_to_bceplugin():
    # Ask the user to select a .zip file
    zip_file_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
    
    if not zip_file_path:
        return  # If no file is selected, do nothing
    
    # Ask for a location to save the .bceplugin file
    save_path = filedialog.asksaveasfilename(defaultextension=".bceplugin", filetypes=[("BCE Plugin Files", "*.bceplugin")])
    
    if not save_path:
        return  # If no save location is selected, do nothing
    
    try:
        # Ensure the selected file is a zip file
        if not zip_file_path.endswith(".zip"):
            messagebox.showerror("Invalid File", "Please select a valid .zip file!")
            return
        
        # Create a new .bceplugin file by renaming the zip file
        bceplugin_file_path = os.path.splitext(save_path)[0] + ".bceplugin"
        
        # Copy the zip file to the new .bceplugin location
        shutil.copy(zip_file_path, bceplugin_file_path)
        
        messagebox.showinfo("Success", f"File converted successfully to {bceplugin_file_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert the file: {e}")

def main():
    # Create the Tkinter window
    root = tk.Tk()
    root.title("ZIP to BCEPlugin Converter")
    root.geometry("400x200")
    
    # Add a label
    label = tk.Label(root, text="Convert a ZIP file to a .bceplugin file", font=("Arial", 14))
    label.pack(pady=20)
    
    # Add a button to trigger the conversion
    convert_button = tk.Button(root, text="Convert ZIP to BCEPlugin", command=convert_to_bceplugin)
    convert_button.pack(pady=10)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
