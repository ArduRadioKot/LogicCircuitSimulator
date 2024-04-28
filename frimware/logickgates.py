import tkinter as tk
from logic_gate import Gate

class LogicGateConstructor:
    def __init__(self, master):
        self.master = master
        self.master.title("Logic Gate Constructor")

        self.gate_types = ['AND', 'OR', 'XOR']
        self.gates = []

        self.canvas = tk.Canvas(self.master, width=800, height=600)
        self.canvas.pack()

        self.create_gate_button()

    def create_gate_button(self):
        gate_button_frame = tk.Frame(self.master)
        gate_button_frame.pack()

        for gate_type in self.gate_types:
            button = tk.Button(gate_button_frame, text=gate_type, command=lambda gate_type=gate_type: self.create_gate(gate_type))
            button.pack(side=tk.LEFT)

    def create_gate(self, gate_type):
        gate = Gate(gate_type)
        self.gates.append(gate)
        gate.create_gate(self.canvas)

class Gate:
    def __init__(self, gate_type):
        self.gate_type = gate_type
        self.inputs = []

    def create_gate(self, canvas):
        x = 100
        y = 100
        width = 100
        height = 50

        gate_id = canvas.create_rectangle(x, y, x + width, y + height, fill='white')
        gate_text_id = canvas.create_text(x + width / 2, y + height / 2, text=self.gate_type, font=('Helvetica', 12))

        for i in range(2):
            input_id = canvas.create_rectangle(x - 20 - i * 30, y - 20, x - 20 - i * 30 + 10, y, fill='white')
            self.inputs.append(input_id)

root = tk.Tk()
app = LogicGateConstructor(root)
root.mainloop()