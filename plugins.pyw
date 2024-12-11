import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import shutil

class PluginManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Plugin Manager")
        self.root.geometry("800x550")
        self.root.resizable(False, False)

        # Plugin directory
        self.plugins_dir = "plugins"
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)

        # UI elements
        self.create_widgets()
        self.load_plugins()

    def create_widgets(self):
        """Create and arrange widgets for the plugin manager."""
        # Title label
        title_label = tk.Label(self.root, text="Plugin Manager", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Listbox to display installed plugins
        self.plugins_listbox = tk.Listbox(self.root, height=10, width=40, selectmode=tk.SINGLE, font=("Arial", 12))
        self.plugins_listbox.pack(pady=10)

        # Buttons frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        # Buttons to load plugins, add new plugin, uninstall selected plugin
        load_button = tk.Button(buttons_frame, text="Load Plugins", command=self.load_plugins, width=20, font=("Arial", 12))
        load_button.grid(row=0, column=0, padx=5)

        new_plugin_button = tk.Button(buttons_frame, text="New Plugin", command=self.new_plugin_action, width=20, font=("Arial", 12))
        new_plugin_button.grid(row=0, column=1, padx=5)

        uninstall_button = tk.Button(buttons_frame, text="Uninstall Plugin", command=self.uninstall_plugin, width=20, font=("Arial", 12))
        uninstall_button.grid(row=1, column=0, columnspan=2, pady=5)

        # Close button
        close_button = tk.Button(self.root, text="Close", command=self.root.quit, width=20, font=("Arial", 12))
        close_button.pack(pady=10)

    def load_plugins(self):
        """Load and display installed plugins."""
        # Clear the listbox before updating
        self.plugins_listbox.delete(0, tk.END)

        try:
            # List all subdirectories in the plugins directory (representing installed plugins)
            plugins = [d for d in os.listdir(self.plugins_dir) if os.path.isdir(os.path.join(self.plugins_dir, d))]
            if not plugins:
                self.plugins_listbox.insert(tk.END, "No plugins installed.")
            else:
                for plugin in plugins:
                    self.plugins_listbox.insert(tk.END, plugin)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load plugins: {e}")

    def new_plugin_action(self):
        """Handle adding a new plugin."""
        # Ask for a .bceplugin file (which is a zip file)
        file_path = filedialog.askopenfilename(filetypes=[("BCE Plugin Files", "*.bceplugin")])

        if not file_path:
            return  # If no file is selected, do nothing

        try:
            # Check if the selected file is a .bceplugin zip file
            if not file_path.endswith(".bceplugin"):
                messagebox.showerror("Invalid File", "Please select a valid .bceplugin file!")
                return

            # Extract the file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Get the original file name (without the .bceplugin extension)
                plugin_name = os.path.splitext(os.path.basename(file_path))[0]
                plugin_folder_path = os.path.join(self.plugins_dir, plugin_name)

                # Create the plugin folder if it doesn't exist
                if not os.path.exists(plugin_folder_path):
                    os.makedirs(plugin_folder_path)

                # Extract contents to the new folder
                zip_ref.extractall(plugin_folder_path)

                messagebox.showinfo("Success", f"Plugin extracted successfully to {plugin_folder_path}")
                self.load_plugins()  # Refresh the plugin list after adding a new one
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract plugin: {e}")

    def uninstall_plugin(self):
        """Uninstall the selected plugin."""
        selected_plugin_index = self.plugins_listbox.curselection()
        if not selected_plugin_index:
            messagebox.showwarning("Select Plugin", "Please select a plugin to uninstall.")
            return

        selected_plugin = self.plugins_listbox.get(selected_plugin_index)

        # Confirm the uninstall action
        confirm = messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to uninstall the plugin '{selected_plugin}'?")
        if confirm:
            plugin_path = os.path.join(self.plugins_dir, selected_plugin)
            try:
                # Delete the plugin folder and its contents
                shutil.rmtree(plugin_path)
                messagebox.showinfo("Success", f"Plugin '{selected_plugin}' uninstalled successfully.")
                self.load_plugins()  # Refresh the list after deletion
            except Exception as e:
                messagebox.showerror("Error", f"Failed to uninstall plugin: {e}")

def run_plugin_manager():
    """Launch the Plugin Manager window."""
    root = tk.Tk()
    plugin_manager = PluginManager(root)
    root.mainloop()

if __name__ == "__main__":
    run_plugin_manager()
