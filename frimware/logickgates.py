import tkinter as tk

class DragAndDropConstructor:
    def __init__(self, master):
        self.master = master
        self.master.title("Logical Scheme Constructor")
        self.master.geometry("800x600")

        self.canvas = tk.Canvas(self.master, width=800, height=600,bg="gray")
        self.canvas.pack(side="left")
        

        self.elements = []

        self.create_draggable_elements()

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

    def create_draggable_elements(self):
        # Create draggable elements (e.g. AND, OR, NOT gates)
        and_gate = tk.Label(self.master, text="AND", bg="gray")
        and_gate.draggable = True
        and_gate.bind("<ButtonPress-1>", self.start_drag)
        and_gate.bind("<ButtonRelease-1>", self.stop_drag)
        and_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(and_gate)

        or_gate = tk.Label(self.master, text="OR", bg="gray")
        or_gate.draggable = True
        or_gate.bind("<ButtonPress-1>", self.start_drag)
        or_gate.bind("<ButtonRelease-1>", self.stop_drag)
        or_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(or_gate)

        not_gate = tk.Label(self.master, text="NOT", bg="gray")
        not_gate.draggable = True
        not_gate.bind("<ButtonPress-1>", self.start_drag)
        not_gate.bind("<ButtonRelease-1>", self.stop_drag)
        not_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(not_gate)

        # Add elements to canvas
        for element in self.elements:
            self.canvas.create_window(10, 10, window=element)

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

    def drag(self, event):
        # Get the element being dragged
        element = event.widget
        element.place(x=event.x, y=event.y)



    def create_and_gate(self):
        and_gate = tk.Label(self.master, text="AND", bg="gray")
        and_gate.draggable = True
        and_gate.bind("<ButtonPress-1>", self.start_drag)
        and_gate.bind("<ButtonRelease-1>", self.stop_drag)
        and_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(and_gate)
        self.canvas.create_window(10, 10, window=and_gate)

    def create_or_gate(self):
        or_gate = tk.Label(self.master, text="OR", bg="gray")
        or_gate.draggable = True
        or_gate.bind("<ButtonPress-1>", self.start_drag)
        or_gate.bind("<ButtonRelease-1>", self.stop_drag)
        or_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(or_gate)
        self.canvas.create_window(10, 10, window=or_gate)

    def create_not_gate(self):
        not_gate = tk.Label(self.master, text="NOT", bg="gray")
        not_gate.draggable = True
        not_gate.bind("<ButtonPress-1>", self.start_drag)
        not_gate.bind("<ButtonRelease-1>", self.stop_drag)
        not_gate.bind("<B1-Motion>", self.drag)
        self.elements.append(not_gate)
        self.canvas.create_window(10, 10, window=not_gate)

root = tk.Tk()
drag_and_drop_constructor = DragAndDropConstructor(root)
root.mainloop()