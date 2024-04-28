import tkinter as tk

class DragAndDrop(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure_master()
        self.initialize_canvas()
        self.add_gate_button()

    def configure_master(self):
        self.master.title("Drag And Drop")
        self.master.iconbitmap("dnd.ico")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

    def initialize_canvas(self):
        self.canvas = tk.Canvas(width=600, height=600, bg="gray")
        self.canvas.pack(side="left")

        self.move_data = {"object": None, "x": 0, "y": 0}

        self.bind_tags("movable")

    def bind_tags(self, tag):
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.move_start)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.move_stop)
        self.canvas.tag_bind(tag, "<B1-Motion>", self.move)

    def move_start(self, event):
        self.move_data["object"] = self.canvas.find_closest(event.x, event.y)[0]
        self.move_data["x"] = event.x
        self.move_data["y"] = event.y
        self.canvas.tag_raise(self.move_data["object"])

    def move_stop(self, event):
        self.move_data["object"] = None
        self.move_data["x"] = 0
        self.move_data["y"] = 0

    def move(self, event):
        dx = event.x - self.move_data["x"]
        dy = event.y - self.move_data["y"]

        self.canvas.move(self.move_data["object"], dx, dy)

        self.move_data["x"] = event.x
        self.move_data["y"] = event.y

    def add_gate_button(self):
        button_frame = tk.Frame(self.master, bg="gray")
        button_frame.pack(side="right", fill="both", expand=True)

        and_button = tk.Button(button_frame, text="AND", command=self.add_and_gate)
        and_button.pack(fill="x")

        or_button = tk.Button(button_frame, text="OR", command=self.add_or_gate)
        or_button.pack(fill="x")

        xor_button = tk.Button(button_frame, text="XOR", command=self.add_xor_gate)
        xor_button.pack(fill="x")

    def add_and_gate(self):
        self.gate = Gate("AND")
        self.gate.create_gate(self.canvas)

    def add_or_gate(self):
        self.gate = Gate("OR")
        self.gate.create_gate(self.canvas)

    def add_xor_gate(self):
        self.gate = Gate("XOR")
        self.gate.create_gate(self.canvas)

class Gate:
    def __init__(self, gate_type):
        self.gate_type = gate_type
        self.inputs = []

    def create_gate(self, canvas):
        x = 100
        y = 100
        width = 100
        height = 50

        gate_id = canvas.create_rectangle(x, y, x + width, y + height, fill='white', tags=("movable", "gate"))
        gate_text_id = canvas.create_text(x + width / 2, y + height /2, text=self.gate_type, font=('Helvetica', 12), fill='black')

        for i in range(2):
            input_id = canvas.create_rectangle(x - 20 - i * 30, y - 20, x - 20 - i * 30 + 10, y, fill='white')
            self.inputs.append(input_id)

        canvas.tag_bind(gate_id, "<ButtonPress-1>", self.move_start)
        canvas.tag_bind(gate_id, "<ButtonRelease-1>", self.move_stop)
        canvas.tag_bind(gate_id, "<B1-Motion>", self.move)

    def move_start(self, event):
        DragAndDrop.move_start(event)

    def move_stop(self, event):
        DragAndDrop.move_stop(event)

    def move(self, event):
        DragAndDrop.move(event)

def main():
    root = tk.Tk()
    app = DragAndDrop(root)
    app.mainloop()

if __name__ == "__main__":
    main()