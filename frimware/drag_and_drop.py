import tkinter as tk
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk




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
    def __init__(self, master):
        self.master = master
        self.master.title("Logical Scheme Constructor")
        self.master.geometry("800x600")
        self.canvas = tk.Canvas(self.master, width=1200, height=1000, bg="gray")
        self.canvas.pack(side="left")
        
        self.elements = []
        self.trash_zone = tk.Frame(self.master, bg="red", width=200, height=200)
        self.trash_zone.pack(side="right", fill="both", expand=True)
        
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()
        self.add_gate_button()



    def add_gate_button(self):
        button_frame = tk.Frame(self.master, bg="gray")
        button_frame.pack(side="right", fill="both", expand=True)

        and_button = tk.Button(button_frame, text="AND", command=self.create_and_gate)
        and_button.pack(fill="x")

        or_button = tk.Button(button_frame, text="OR", command=self.create_or_gate)
        or_button.pack(fill="x")

        xor_button = tk.Button(button_frame, text="XOR", command=self.create_not_gate)
        xor_button.pack(fill="x")


  
        save_button = tk.Button(button_frame, text="Save", command=self.save_logical_elements)
        save_button.pack(fill="x")

        open_button = tk.Button(button_frame, text="Open", command=self.open_logical_elements)
        open_button.pack(fill="x")

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_logical_elements)
        delete_button.pack(fill="x")
#===============================================================================
    # def create_draggable_elements(self):
    #     # Create draggable elements (e.g. AND, OR, NOT gates)
    #     and_gate = tk.Label(self.master, text="AND", bg="white", fg="black")
    #     and_gate.draggable = True
    #     and_gate.bind("<ButtonPress-1>", self.start_drag)
    #     and_gate.bind("<ButtonRelease-1>", self.stop_drag)
    #     and_gate.bind("<B1-Motion>", self.drag)
    #     self.elements.append(and_gate)

    #     or_gate = tk.Label(self.master, text="OR", bg="white", fg="black")
    #     or_gate.draggable = True
    #     or_gate.bind("<ButtonPress-1>", self.start_drag)
    #     or_gate.bind("<ButtonRelease-1>", self.stop_drag)
    #     or_gate.bind("<B1-Motion>", self.drag)
    #     self.elements.append(or_gate)

    #     not_gate = tk.Label(self.master, text="NOT", bg="white", fg="black")
    #     not_gate.draggable = True
    #     not_gate.bind("<ButtonPress-1>", self.start_drag)
    #     not_gate.bind("<ButtonRelease-1>", self.stop_drag)
    #     not_gate.bind("<B1-Motion>", self.drag)
    #     self.elements.append(not_gate)

        # # Add elements to canvas
        # for element in self.elements:
        #     self.canvas.create_window(10, 10, window=element)
#============================================================
    def start_drag(self, event):
        # Get the element being dragged
        element = event.widget
        element.x = event.x
        element.y = event.y

    def stop_drag(self, event):
        # Get the element being dragged
        element = event.widget
        element.x = event.x
        element.y = event.y
        if self.is_in_trash_zone(element):
            self.delete_element(element)

    def drag(self, event):
        # Get the element being dragged
        element = event.widget
        element.place(x=event.x, y=event.y)



    def create_and_gate(self):
        and_gate = tk.Label(self.master, text="AND", bg="white", fg="black")
        and_gate.draggable = True
        and_gate.bind("<ButtonPress-1>", self.start_drag)
        and_gate.bind("<ButtonRelease-1>", self.stop_drag)
        and_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(and_gate)
        self.canvas.create_window(10, 10, window=and_gate)

    def create_or_gate(self):
        or_gate = tk.Label(self.master, text="OR", bg="white", fg="black")
        or_gate.draggable = True
        or_gate.bind("<ButtonPress-1>", self.start_drag)
        or_gate.bind("<ButtonRelease-1>", self.stop_drag)
        or_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(or_gate)
        self.canvas.create_window(10, 10, window=or_gate)

    def create_not_gate(self):
        not_gate = tk.Label(self.master, text="NOT", bg="white", fg="black")
        not_gate.draggable = True
        not_gate.bind("<ButtonPress-1>", self.start_drag)
        not_gate.bind("<ButtonRelease-1>", self.stop_drag)
        not_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(not_gate)
        self.canvas.create_window(10, 10, window=not_gate)


    def save_logical_elements(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".lcs", filetypes=[ ('LogicCircuitSimulator', '*.lcs')])
        if file_path:
             with open(file_path, "w") as f:
                  for element in self.elements:
                   x, y = element.winfo_x(), element.winfo_y()
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
                    element = tk.Label(self.master, text=text, bg="white", fg="black")
                    element.place(x=x, y=y)
                    self.elements.append(element)


    def delete_logical_elements(self):
        for element in self.elements:
            element.destroy()
        self.elements = []


    def is_in_trash_zone(self, element):
        x, y = element.winfo_x(), element.winfo_y()
        return (x > self.trash_zone.winfo_x() and
                x < self.trash_zone.winfo_x() + self.trash_zone.winfo_width() and
                y > self.trash_zone.winfo_y() and
                y < self.trash_zone.winfo_y() + self.trash_zone.winfo_height())

    def delete_element(self, element):
        element.destroy()
        self.elements.remove(element)



        
root = tk.Tk()
drag_and_drop_constructor = DragAndDropConstructor(root)
root.mainloop()