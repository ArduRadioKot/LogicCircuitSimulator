import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.scrolledtext import ScrolledText

#======================================
# root = tk.Tk()
# root.geometry('800x600')

# img = Image.open('Sim.ico')
# tk_img = ImageTk.PhotoImage(img)


# label = tk.Label(root, image=tk_img)
# label.pack()


# root.after(5000, root.destroy)


# root.mainloop()


#========================================

class DragAndDropConstructor:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.root = master
        self.master.title("Logical Scheme Constructor")
        self.master.geometry("800x600")
        self.toolbar = tk.Frame(self.master, bg="gray")
        self.toolbar.pack(fill="x")

        # Кнопка "Открыть файл"
        self.open_button = tk.Button(self.toolbar, text="Open file", command=self.open_logical_elements)
        self.open_button.pack(side="left", padx=5, pady=5)

        # Кнопка "Создать файл"
        self.create_button = tk.Button(self.toolbar, text="Save file", command=self.save_logical_elements)
        self.create_button.pack(side="left", padx=5, pady=5)

        # Кнопка "Удалить файл"
        self.delete_button = tk.Button(self.toolbar, text="Settings", command=self.settings)
        self.delete_button.pack(side="left", padx=5, pady=5)

        self.delete_button = tk.Button(self.toolbar, text="Clear", command=self.delete_logical_elements)
        self.delete_button.pack(side="left", padx=5, pady=5)

        self.delete_button = tk.Button(self.toolbar, text="Quit", command=quit)
        self.delete_button.pack(side="left", padx=5, pady=5)

        self.canvas = tk.Canvas(self.master, width=1200, height=1000000, bg="gray")
        self.canvas.pack(side="left")
        self.scroll_region = (0, 0, 1000, 1000)  # Set the scroll region to be larger than the canvas size
        self.canvas.config(scrollregion=self.scroll_region)
        
        self.elements = []
        self.trash_zone = tk.Frame(self.master, bg="red", width=200, height=200)
        self.trash_zone.pack(side="right", fill="both", expand=True)
        
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()
        self.v_scroll = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.v_scroll.set)
        self.add_gate_button()

    def quit(self):
        self.root.destroy
        

    def add_gate_button(self):
        button_frame = tk.Frame(self.master, bg="gray")
        button_frame.pack(side="right", fill="both", expand=True)

        and_button = tk.Button(button_frame, text="AND", command=self.create_and_gate)
        and_button.pack(fill="x")

        or_button = tk.Button(button_frame, text="OR", command=self.create_or_gate)
        or_button.pack(fill="x")

        xor_button = tk.Button(button_frame, text="NOT", command=self.create_not_gate)
        xor_button.pack(fill="x")

        xor_button = tk.Button(button_frame, text="XOR", command=self.create_xor_gate)
        xor_button.pack(fill="x")

        create_custom_button = tk.Button(button_frame, text="Create Custom Element", command=self.create_custom_element)
        create_custom_button.pack()

    def create_and_gate(self):
        and_gate = tk.Label(self.master, text="AND", bg="white", fg="black", width=5, height=2)
        and_gate.draggable = True
        and_gate.bind("<ButtonPress-1>", self.start_drag)
        and_gate.bind("<ButtonRelease-1>", self.stop_drag)
        and_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(and_gate)
        self.canvas.create_window(10, 10, window=and_gate)

    def create_or_gate(self):
        or_gate = tk.Label(self.master, text="OR", bg="white", fg="black", width=5, height=2)
        or_gate.draggable = True
        or_gate.bind("<ButtonPress-1>",self.start_drag)
        or_gate.bind("<ButtonRelease-1>", self.stop_drag)
        or_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(or_gate)
        self.canvas.create_window(10, 10, window=or_gate)

    def create_not_gate(self):
        not_gate = tk.Label(self.master, text="NOT", bg="white", fg="black", width=5, height=2)
        not_gate.draggable = True
        not_gate.bind("<ButtonPress-1>", self.start_drag)
        not_gate.bind("<ButtonRelease-1>", self.stop_drag)
        not_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(not_gate)
        self.canvas.create_window(10, 10, window=not_gate)

    def create_xor_gate(self):
        not_gate = tk.Label(self.master, text="xor", bg="white", fg="black", width=5, height=2)
        not_gate.draggable = True
        not_gate.bind("<ButtonPress-1>", self.start_drag)
        not_gate.bind("<ButtonRelease-1>", self.stop_drag)
        not_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(not_gate)
        self.canvas.create_window(10, 10, window=not_gate)

    def start_drag(self, event: tk.Event):
        element = event.widget
        element.x0 = event.x
        element.y0 = event.y

    def stop_drag(self, event: tk.Event):
        element = event.widget
        if self.is_in_trash_zone(element):
            self.delete_element(element)

    def drag(self, event: tk.Event):
        element = event.widget
        dx = event.x - element.x0
        dy = event.y - element.y0
        element.place(x=element.winfo_x() + dx, y=element.winfo_y() + dy)
        element.x0 = event.x
        element.y0 = event.y

    def save_logical_elements(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".lcs", filetypes=[('LogicCircuitSimulator', '*.lcs')])
        if file_path:
            with open(file_path, "w") as f:
                for element in self.elements:
                    x, y = element.winfo_rootx(), element.winfo_rooty()
                    f.write(f"{element.cget('text')} {x} {y}\n")
            print("Logical scheme saved to logical_scheme.lgs")

    def open_logical_elements(self):
        file_path = filedialog.askopenfilename(filetypes=[("LogicCircuitSimulator files", "*.lcs")])
        if file_path:
            self.elements = []
            with open(file_path, "r") as f:
                for line in f:
                    text, x, y = line.strip().split()
                    x, y = int(x), int(y)
                    element = tk.Label(self.master, text=text, bg="white", fg="black", width=5, height=2)
                    element.place(x=x, y=y)
                    element.draggable = True
                    element.bind("<ButtonPress-1>", self.start_drag)
                    element.bind("<ButtonRelease-1>", self.stop_drag)
                    element.bind("<B1-Motion>", self.drag)
                    self.elements.append(element)

    def delete_logical_elements(self):
        for element in self.elements:
            element.destroy()
        self.elements = []

    def is_in_trash_zone(self, element: tk.Label):
        x, y = element.winfo_x(), element.winfo_y()
        return (x > self.trash_zone.winfo_x() and
                x < self.trash_zone.winfo_x() + self.trash_zone.winfo_width() and
                y > self.trash_zone.winfo_y() and
                y < self.trash_zone.winfo_y() + self.trash_zone.winfo_height())

    def delete_element(self, element: tk.Label):
        element.destroy()
        self.elements.remove(element)


    def create_custom_element(self):
        custom_element_window = tk.Toplevel(self.master)
        custom_element_window.title("Create Custom Logical Element")

        text_editor = ScrolledText(custom_element_window, width=40, height=10)
        text_editor.pack(fill="both", expand=True)

        create_button = tk.Button(custom_element_window, text="Create", command=lambda: self.add_custom_element(text_editor.get("1.0", "end-1c")))
        create_button.pack()

    def add_custom_element(self, element_text: str):
        custom_element = tk.Text(self.master, width=20, height=5)
        custom_element.insert("1.0", element_text)
        custom_element.draggable = True
        custom_element.bind("<ButtonPress-1>", self.start_drag)
        custom_element.bind("<ButtonRelease-1>", self.stop_drag)
        custom_element.bind("<B1-Motion>", self.drag)
        self.elements.append(custom_element)
        self.canvas.create_window(10, 10, window=custom_element)
    # Save the custom element's source code to a separate Python file
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[('Python files', '*.py')])
        if file_path:
             with open(file_path, "w") as f:
                  f.write(f"custom_element = tk.Label(self.master, text='{element_text}', bg='white', fg='black')\n")
                  f.write("custom_element.draggable = True\n")
                  f.write("custom_element.bind('<ButtonPress-1>', self.start_drag)\n")
                  f.write("custom_element.bind('<ButtonRelease-1>', self.stop_drag)\n")
                  f.write("custom_element.bind('<B1-Motion>', self.drag)\n")
                  f.write("self.elements.append(custom_element)\n")
                  f.write("self.canvas.create_window(10, 10, window=custom_element)\n")

    def settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")

        # Theme selection
        tk.Label(settings_window, text="Theme:").pack()
        theme_var = tk.StringVar()
        theme_var.set("Default")  # default theme
        theme_options = ["Default", "Dark", "Light", "Custom"]
        theme_menu = tk.OptionMenu(settings_window, theme_var, *theme_options)
        theme_menu.pack()

        # Apply theme button
        def apply_theme():
            theme = theme_var.get()
            if theme == "Dark":
                self.master.configure(bg="gray")
                self.toolbar.configure(bg="#15294a")
                self.canvas.configure(bg="#2d3d52")

            elif theme == "Light":
                self.master.configure(bg="white")
                self.toolbar.configure(bg="#244275")
                self.canvas.configure(bg="#6d90bd")
           
            elif theme == "Custom":
                # Add custom theme options here
                pass
            else:
                self.master.configure(bg="SystemButtonFace")
                self.toolbar.configure(bg="SystemButtonFace")
                self.canvas.configure(bg="SystemButtonFace")
                

        tk.Button(settings_window, text="Apply", command=apply_theme).pack()

        tk.Button(settings_window, text="OK", command=settings_window.destroy).pack()


root = tk.Tk()
drag_and_drop_constructor = DragAndDropConstructor(root)
root.mainloop()