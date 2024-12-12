import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
import os

# Ensure required modules are installed
def ensure_dependencies():
    required_modules = ["openai"]
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to install required module '{module}': {e}")
                sys.exit(1)

ensure_dependencies()

import openai  # Example for OpenAI integration (placeholder)

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Code Editor")
        self.root.geometry("800x600")

        # Create a Text widget for code editing
        self.text_area = tk.Text(root, wrap="none", undo=True, font=("Courier New", 12))
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        # Add line numbers
        self.line_numbers = tk.Text(root, width=4, padx=3, takefocus=0, border=0, background="lightgray", state="disabled")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Add a vertical scrollbar
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        # Add a horizontal scrollbar
        self.h_scrollbar = tk.Scrollbar(self.text_area, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.config(xscrollcommand=self.h_scrollbar.set)
        self.h_scrollbar.config(command=self.text_area.xview)

        # Bind events for updating line numbers and indentation
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<Return>", self.handle_return)
        self.text_area.bind("<Tab>", self.insert_tab)
        self.text_area.bind("<BackSpace>", self.handle_backspace)

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        # Add Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.root.focus_get().event_generate('<<Cut>>'))
        edit_menu.add_command(label="Copy", command=lambda: self.root.focus_get().event_generate('<<Copy>>'))
        edit_menu.add_command(label="Paste", command=lambda: self.root.focus_get().event_generate('<<Paste>>'))

        # Add Tools menu
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="BCE Plugins Converter", command=self.open_bceplugin_converter)
        tools_menu.add_command(label="Plugins", command=self.open_plugins_window)

        # Add AI menu
        ai_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="AI", menu=ai_menu)
        ai_menu.add_command(label="Login to AI", command=self.login_to_ai)
        ai_menu.add_command(label="Ask AI", command=self.ask_ai_help)

        # Store the current file path
        self.file_path = None

        # Placeholder for AI API key
        self.ai_api_key = None

        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete(1.0, tk.END)
        line_count = int(self.text_area.index("end-1c").split(".")[0])
        for line in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{line}\n")
        self.line_numbers.config(state="disabled")

    def insert_tab(self, event):
        self.text_area.insert(tk.INSERT, "    ")
        return "break"

    def handle_return(self, event):
        current_line = self.text_area.get("insert linestart", "insert")
        indent = "".join([char for char in current_line if char in " \t"])
        self.text_area.insert("insert", "\n" + indent)
        return "break"

    def handle_backspace(self, event):
        cursor_index = self.text_area.index("insert")
        col = int(cursor_index.split(".")[1])
        if col > 0 and col % 4 == 0:
            prev_chars = self.text_area.get(f"insert-{col % 4}c", "insert")
            if prev_chars == "    ":
                self.text_area.delete(f"insert-{col % 4}c", "insert")
                return "break"

    def open_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, 'r') as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.file_path = file_path
                self.root.title(f"Basic Code Editor - {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, 'w') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content.strip())
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, 'w') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content.strip())
                self.file_path = file_path
                self.root.title(f"Basic Code Editor - {file_path}")
                messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def login_to_ai(self):
        try:
            self.ai_api_key = filedialog.askstring("AI Login", "Enter your AI API Key:")
            if self.ai_api_key:
                messagebox.showinfo("Success", "AI API Key set successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set AI API Key: {e}")

    def ask_ai_help(self):
        if not self.ai_api_key:
            messagebox.showwarning("AI Login", "Please login with your AI API Key first.")
            return

        prompt = self.text_area.get("1.0", "end-1c")
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150
            )
            messagebox.showinfo("AI Response", response.choices[0].text.strip())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get AI response: {e}")

    def open_bceplugin_converter(self):
        # Open the bceplugin.py script using subprocess
        try:
            subprocess.Popen([sys.executable, "bceplugin.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open BCE Plugin Converter: {e}")

    def open_plugins_window(self):
        # Open the plugins.pyw script using subprocess
        try:
            subprocess.Popen([sys.executable, "plugins.pyw"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Plugins window: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()
