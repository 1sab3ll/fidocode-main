import tkinter as tk

def show_about():
    about_window = tk.Tk()
    about_window.title("About")
    about_window.geometry("400x200")
    label = tk.Label(about_window, text="Basic Code Editor\nVersion 1.0\nCreated by You!", font=("Arial", 14))
    label.pack(pady=40)
    button = tk.Button(about_window, text="Close", command=about_window.quit)
    button.pack(pady=10)
    about_window.mainloop()

if __name__ == "__main__":
    show_about()
