# Import the tkinter module
import tkinter as tk

# Create a new tkinter window
window = tk.Tk()

# Create a text widget
text_widget = tk.Text(window)

# Add the text widget to the window
text_widget.pack()

# Create a function to save the contents of the text widget to a file
def save_file():
    file = tk.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if file is None:
        return
    file.write(text_widget.get("1.0", "end-1c"))
    file.close()

# Create a menu with a "File" dropdown
menu = tk.Menu(window)
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=save_file)

# Add the menu to the window
window.config(menu=menu)

# Start the tkinter event loop
window.mainloop()