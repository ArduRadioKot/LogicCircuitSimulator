import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import math

class LogicalElement:
    def __init__(self, canvas, x, y, element_type):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.element_type = element_type
        self.inputs = []
        self.output = None
        self.value = False
        self.rect = None  # Store rectangle reference
        self.text = None  # Store text reference
        self.button_highlight = None
        self.create_visual()
        
    def create_visual(self):
        if self.element_type == "AND":
            self.draw_and_gate()
        elif self.element_type == "OR":
            self.draw_or_gate()
        elif self.element_type == "NOT":
            self.draw_not_gate()
        elif self.element_type == "XOR":
            self.draw_xor_gate()
        elif self.element_type == "INPUT":
            self.draw_input_device()
        elif self.element_type == "OUTPUT":
            self.draw_output_device()
            
    def draw_and_gate(self):
        # Draw simple rectangle for AND gate
        self.rect = self.canvas.create_rectangle(self.x, self.y, self.x+40, self.y+40, 
                                   fill="white", outline="black")
        self.text = self.canvas.create_text(self.x+20, self.y+20, text="AND", fill="black")
        
        # Create input ports
        self.inputs = [
            self.create_port(self.x, self.y+10, "input"),
            self.create_port(self.x, self.y+30, "input")
        ]
        # Create output port
        self.output = self.create_port(self.x+40, self.y+20, "output")
        
    def draw_or_gate(self):
        # Draw simple rectangle for OR gate
        self.rect = self.canvas.create_rectangle(self.x, self.y, self.x+40, self.y+40, 
                                   fill="white", outline="black")
        self.text = self.canvas.create_text(self.x+20, self.y+20, text="OR", fill="black")
        
        # Create input ports
        self.inputs = [
            self.create_port(self.x, self.y+10, "input"),
            self.create_port(self.x, self.y+30, "input")
        ]
        # Create output port
        self.output = self.create_port(self.x+40, self.y+20, "output")
        
    def draw_not_gate(self):
        # Draw simple rectangle for NOT gate
        self.rect = self.canvas.create_rectangle(self.x, self.y, self.x+40, self.y+40, 
                                   fill="white", outline="black")
        self.text = self.canvas.create_text(self.x+20, self.y+20, text="NOT", fill="black")
        
        # Create input port
        self.inputs = [self.create_port(self.x, self.y+20, "input")]
        # Create output port
        self.output = self.create_port(self.x+40, self.y+20, "output")
        
    def draw_xor_gate(self):
        # Draw simple rectangle for XOR gate
        self.rect = self.canvas.create_rectangle(self.x, self.y, self.x+40, self.y+40, 
                                   fill="white", outline="black")
        self.text = self.canvas.create_text(self.x+20, self.y+20, text="XOR", fill="black")
        
        # Create input ports
        self.inputs = [
            self.create_port(self.x, self.y+10, "input"),
            self.create_port(self.x, self.y+30, "input")
        ]
        # Create output port
        self.output = self.create_port(self.x+40, self.y+20, "output")
        
    def draw_input_device(self):
        # Draw input device (button)
        self.rect = self.canvas.create_rectangle(self.x, self.y, self.x+40, self.y+40, 
                                   fill="white", outline="black")
        self.text = self.canvas.create_text(self.x+20, self.y+20, text="IN", fill="black")
        
        # Create output port
        self.output = self.create_port(self.x+40, self.y+20, "output")
        
        # Add button-like appearance
        self.button_highlight = self.canvas.create_rectangle(
            self.x+2, self.y+2, self.x+38, self.y+38,
            fill="", outline="gray"
        )
        
    def draw_output_device(self):
        # Draw LED symbol (circle with input)
        self.rect = self.canvas.create_oval(self.x, self.y, self.x+40, self.y+40, 
                                          fill="white", outline="black")
        self.text = self.canvas.create_text(self.x+20, self.y+20, text="LED", fill="black")
        
        # Create input port
        self.inputs = [self.create_port(self.x, self.y+20, "input")]
        
    def create_port(self, x, y, port_type):
        port = self.canvas.create_oval(x-5, y-5, x+5, y+5, 
                                     fill="gray", outline="black")
        self.canvas.tag_bind(port, "<Button-1>", 
                           lambda e: self.on_port_click(port, port_type))
        return port
        
    def on_port_click(self, port, port_type):
        if self.simulation_mode:
            if port_type == "input":
                # Toggle input value in simulation mode
                element = self.find_element_by_port(port)
                if element and element.element_type == "INPUT":
                    element.value = not element.value
                    # Update button appearance
                    if element.value:
                        self.canvas.itemconfig(element.rect, fill="#e0e0e0")
                        self.canvas.itemconfig(element.button_highlight, outline="black")
                        self.canvas.itemconfig(element.output, fill="green")
                    else:
                        self.canvas.itemconfig(element.rect, fill="white")
                        self.canvas.itemconfig(element.button_highlight, outline="gray")
                        self.canvas.itemconfig(element.output, fill="gray")
                    self.update_simulation()
            return
            
        if self.selected_port is None:
            self.selected_port = (port, port_type)
            self.canvas.itemconfig(port, fill="green")
            self.status_label.config(text="Select second port")
        else:
            if self.selected_port[0] == port:
                # Deselect if clicking the same port
                self.canvas.itemconfig(port, fill="gray")
                self.selected_port = None
                self.status_label.config(text="Ready")
                return
                
            # Create connection
            if self.is_valid_connection(self.selected_port[1], port_type):
                self.create_connection(self.selected_port[0], port)
                self.status_label.config(text="Connection created")
            else:
                self.status_label.config(text="Invalid connection")
                
            # Reset selection
            self.canvas.itemconfig(self.selected_port[0], fill="gray")
            self.selected_port = None
            self.status_label.config(text="Ready")

    def evaluate(self, connections):
        if self.element_type == "AND":
            # Get values from connected input elements
            input_values = []
            for input_port in self.inputs:
                # Find connected output port
                for conn in connections:
                    if conn[2] == input_port:  # If this input port is connected
                        # Find the element that owns the output port
                        for element in self.elements:
                            if conn[1] == element.output:
                                input_values.append(element.value)
                                break
            return all(input_values)
        elif self.element_type == "OR":
            # Get values from connected input elements
            input_values = []
            for input_port in self.inputs:
                # Find connected output port
                for conn in connections:
                    if conn[2] == input_port:  # If this input port is connected
                        # Find the element that owns the output port
                        for element in self.elements:
                            if conn[1] == element.output:
                                input_values.append(element.value)
                                break
            return any(input_values)
        elif self.element_type == "NOT":
            # Get value from connected input element
            for conn in connections:
                if conn[2] == self.inputs[0]:  # If this input port is connected
                    # Find the element that owns the output port
                    for element in self.elements:
                        if conn[1] == element.output:
                            return not element.value
            return False
        elif self.element_type == "XOR":
            # Get values from connected input elements
            input_values = []
            for input_port in self.inputs:
                # Find connected output port
                for conn in connections:
                    if conn[2] == input_port:  # If this input port is connected
                        # Find the element that owns the output port
                        for element in self.elements:
                            if conn[1] == element.output:
                                input_values.append(element.value)
                                break
            return sum(input_values) % 2 == 1
        elif self.element_type == "INPUT":
            return self.value
        elif self.element_type == "OUTPUT":
            # Get value from connected input element
            for conn in connections:
                if conn[2] == self.inputs[0]:  # If this input port is connected
                    # Find the element that owns the output port
                    for element in self.elements:
                        if conn[1] == element.output:
                            return element.value
            return False
        return False

    def move(self, dx, dy):
        # Move the element and all its components
        self.x += dx
        self.y += dy
        
        # Move rectangle/oval
        if self.element_type == "OUTPUT":
            self.canvas.coords(self.rect, self.x, self.y, self.x+40, self.y+40)
        else:
            self.canvas.coords(self.rect, self.x, self.y, self.x+40, self.y+40)
            if self.element_type == "INPUT":
                # Move button highlight
                self.canvas.coords(self.button_highlight, 
                                 self.x+2, self.y+2, 
                                 self.x+38, self.y+38)
        
        # Move text
        self.canvas.coords(self.text, self.x+20, self.y+20)
        
        # Move ports based on element type
        if self.element_type == "INPUT":
            # Move output port for input element
            self.canvas.coords(self.output, 
                             self.x+40-5, self.y+20-5,
                             self.x+40+5, self.y+20+5)
        elif self.element_type == "OUTPUT":
            # Move input port for output element
            self.canvas.coords(self.inputs[0], 
                             self.x-5, self.y+20-5,
                             self.x+5, self.y+20+5)
        elif self.element_type == "NOT":
            # Move input port for NOT gate
            self.canvas.coords(self.inputs[0], 
                             self.x-5, self.y+20-5,
                             self.x+5, self.y+20+5)
            # Move output port
            self.canvas.coords(self.output, 
                             self.x+40-5, self.y+20-5,
                             self.x+40+5, self.y+20+5)
        else:
            # Move input ports for other gates
            self.canvas.coords(self.inputs[0], 
                             self.x-5, self.y+10-5,
                             self.x+5, self.y+10+5)
            self.canvas.coords(self.inputs[1], 
                             self.x-5, self.y+30-5,
                             self.x+5, self.y+30+5)
            # Move output port
            self.canvas.coords(self.output, 
                             self.x+40-5, self.y+20-5,
                             self.x+40+5, self.y+20+5)

class LogicCircuitSimulator:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.root = master
        self.master.title("Logic Circuit Simulator")
        self.master.geometry("1200x800")
        
        # Create main frames
        self.create_toolbar()
        self.create_canvas()
        self.create_sidebar()
        
        self.elements = []
        self.connections = []
        self.selected_port = None
        self.dragging_element = None
        self.simulation_mode = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.selected_element = None  # Add selected element tracking
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        # Add Delete key binding
        self.master.bind("<Delete>", self.delete_selected_element)
        
    def create_toolbar(self):
        self.toolbar = tk.Frame(self.master, bg="gray", height=40)
        self.toolbar.pack(fill="x", padx=5, pady=5)
        
        # File operations
        tk.Button(self.toolbar, text="New", command=self.new_scheme).pack(side="left", padx=5)
        tk.Button(self.toolbar, text="Open", command=self.open_scheme).pack(side="left", padx=5)
        tk.Button(self.toolbar, text="Save", command=self.save_scheme).pack(side="left", padx=5)
        
        # Simulation controls
        self.sim_button = tk.Button(self.toolbar, text="Start Simulation", 
                                  command=self.toggle_simulation)
        self.sim_button.pack(side="left", padx=5)
        
        # Status label
        self.status_label = tk.Label(self.toolbar, text="Ready", bg="gray", fg="white")
        self.status_label.pack(side="right", padx=5)
        
    def create_canvas(self):
        # Create canvas with scrollbars
        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=800, height=600)
        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient="vertical", 
                                   command=self.canvas.yview)
        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient="horizontal", 
                                   command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=self.v_scroll.set,
                            xscrollcommand=self.h_scroll.set)
        
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.master, bg="lightgray", width=200)
        self.sidebar.pack(side="right", fill="y", padx=5, pady=5)
        
        # Add element buttons
        tk.Label(self.sidebar, text="Elements", bg="lightgray").pack(pady=5)
        tk.Button(self.sidebar, text="Input", 
                 command=lambda: self.create_element("INPUT")).pack(fill="x", padx=5, pady=2)
        tk.Button(self.sidebar, text="Output (LED)", 
                 command=lambda: self.create_element("OUTPUT")).pack(fill="x", padx=5, pady=2)
        tk.Button(self.sidebar, text="AND Gate", 
                 command=lambda: self.create_element("AND")).pack(fill="x", padx=5, pady=2)
        tk.Button(self.sidebar, text="OR Gate", 
                 command=lambda: self.create_element("OR")).pack(fill="x", padx=5, pady=2)
        tk.Button(self.sidebar, text="NOT Gate", 
                 command=lambda: self.create_element("NOT")).pack(fill="x", padx=5, pady=2)
        tk.Button(self.sidebar, text="XOR Gate", 
                 command=lambda: self.create_element("XOR")).pack(fill="x", padx=5, pady=2)
        
        # Add clear button
        tk.Button(self.sidebar, text="Clear All", 
                 command=self.clear_scheme).pack(fill="x", padx=5, pady=20)
        
    def create_element(self, element_type):
        element = LogicalElement(self.canvas, 50, 50, element_type)
        element.on_port_click = self.on_port_click
        self.elements.append(element)
        
    def on_port_click(self, port, port_type):
        if self.simulation_mode:
            if port_type == "input":
                # Toggle input value in simulation mode
                element = self.find_element_by_port(port)
                if element and element.element_type == "INPUT":
                    element.value = not element.value
                    # Update button appearance
                    if element.value:
                        self.canvas.itemconfig(element.rect, fill="#e0e0e0")
                        self.canvas.itemconfig(element.button_highlight, outline="black")
                        self.canvas.itemconfig(element.output, fill="green")
                    else:
                        self.canvas.itemconfig(element.rect, fill="white")
                        self.canvas.itemconfig(element.button_highlight, outline="gray")
                        self.canvas.itemconfig(element.output, fill="gray")
                    self.update_simulation()
            return
            
        if self.selected_port is None:
            self.selected_port = (port, port_type)
            self.canvas.itemconfig(port, fill="green")
            self.status_label.config(text="Select second port")
        else:
            if self.selected_port[0] == port:
                # Deselect if clicking the same port
                self.canvas.itemconfig(port, fill="gray")
                self.selected_port = None
                self.status_label.config(text="Ready")
                return
                
            # Create connection
            if self.is_valid_connection(self.selected_port[1], port_type):
                self.create_connection(self.selected_port[0], port)
                self.status_label.config(text="Connection created")
            else:
                self.status_label.config(text="Invalid connection")
                
            # Reset selection
            self.canvas.itemconfig(self.selected_port[0], fill="gray")
            self.selected_port = None
            self.status_label.config(text="Ready")

    def is_valid_connection(self, port1_type, port2_type):
        # Check if trying to connect output to input
        if port1_type == "output" and port2_type == "input":
            return True
        # Check if trying to connect input to output
        if port1_type == "input" and port2_type == "output":
            return True
        return False
               
    def create_connection(self, start_port, end_port):
        try:
            # Get coordinates
            start_coords = self.canvas.coords(start_port)
            end_coords = self.canvas.coords(end_port)
            
            if not start_coords or not end_coords:
                self.status_label.config(text="Error: Invalid port coordinates")
                return
                
            # Create line
            line = self.canvas.create_line(
                (start_coords[0] + start_coords[2])/2,
                (start_coords[1] + start_coords[3])/2,
                (end_coords[0] + end_coords[2])/2,
                (end_coords[1] + end_coords[3])/2,
                fill="black", width=2
            )
            
            # Bind right-click event to delete connection
            self.canvas.tag_bind(line, "<Button-3>", lambda e: self.delete_connection(line))
            
            # Store connection
            self.connections.append((line, start_port, end_port))
            
            # Update simulation if in simulation mode
            if self.simulation_mode:
                self.update_simulation()
                
            self.status_label.config(text="Connection created")
        except Exception as e:
            self.status_label.config(text=f"Error creating connection: {str(e)}")
            # Reset selection
            if self.selected_port:
                self.canvas.itemconfig(self.selected_port[0], fill="gray")
                self.selected_port = None

    def delete_connection(self, line):
        # Find and remove the connection
        for i, conn in enumerate(self.connections):
            if conn[0] == line:
                # Delete the line from canvas
                self.canvas.delete(line)
                # Remove from connections list
                self.connections.pop(i)
                # Update simulation if in simulation mode
                if self.simulation_mode:
                    self.update_simulation()
                break

    def find_element_by_port(self, port):
        for element in self.elements:
            if port in element.inputs or port == element.output:
                return element
        return None
        
    def toggle_simulation(self):
        self.simulation_mode = not self.simulation_mode
        if self.simulation_mode:
            self.sim_button.config(text="Stop Simulation")
            self.status_label.config(text="Simulation mode - Click on input elements to toggle")
            # Reset all elements to initial state
            for element in self.elements:
                if element.element_type == "INPUT":
                    element.value = False
                    self.canvas.itemconfig(element.rect, fill="white")
                    self.canvas.itemconfig(element.button_highlight, outline="gray")
                    self.canvas.itemconfig(element.output, fill="gray")
                elif element.element_type == "OUTPUT":
                    self.canvas.itemconfig(element.rect, fill="white")
                else:
                    self.canvas.itemconfig(element.output, fill="gray")
            # Initial simulation update
            self.update_simulation()
        else:
            self.sim_button.config(text="Start Simulation")
            self.status_label.config(text="Ready")
            
    def update_simulation(self):
        if not self.simulation_mode:
            return

        # Создаем словарь для хранения входных значений каждого элемента
        input_values = {element: [] for element in self.elements}
        
        # Создаем словарь для хранения выходных значений каждого элемента
        output_values = {element: element.value for element in self.elements}

        # Собираем все входные значения для каждого элемента
        for conn in self.connections:
            start_port = conn[1]
            end_port = conn[2]
            
            # Находим элементы, соединенные через эти порты
            start_element = None
            end_element = None
            
            for element in self.elements:
                if start_port == element.output:
                    start_element = element
                if end_port in element.inputs:
                    end_element = element
                    
            if start_element and end_element:
                input_values[end_element].append(output_values[start_element])

        # Обрабатываем каждый элемент
        for element in self.elements:
            if element.element_type == "INPUT":
                continue  # Пропускаем входные элементы, их значения уже установлены

            # Получаем входные значения для элемента
            inputs = input_values[element]
            
            # Вычисляем выходное значение в зависимости от типа элемента
            if element.element_type == "AND":
                element.value = all(inputs) if inputs else False
            elif element.element_type == "OR":
                element.value = any(inputs) if inputs else False
            elif element.element_type == "NOT":
                element.value = not inputs[0] if inputs else False
            elif element.element_type == "XOR":
                element.value = sum(inputs) % 2 == 1 if inputs else False
            elif element.element_type == "OUTPUT":
                # Для светодиода берем значение с входа
                if inputs:
                    element.value = inputs[0]
                else:
                    element.value = False

            # Обновляем выходное значение в словаре
            output_values[element] = element.value

            # Обновляем визуальное состояние элемента
            if element.element_type == "OUTPUT":
                if element.value:
                    # Если на входе 1 - светодиод красный
                    self.canvas.itemconfig(element.rect, fill="red", outline="red")
                    self.canvas.itemconfig(element.text, fill="white")
                else:
                    # Если на входе 0 - светодиод белый
                    self.canvas.itemconfig(element.rect, fill="white", outline="black")
                    self.canvas.itemconfig(element.text, fill="black")
            else:
                # Для логических элементов обновляем цвет выходного порта
                color = "green" if element.value else "gray"
                self.canvas.itemconfig(element.output, fill=color)

    def new_scheme(self):
        if messagebox.askyesno("New Scheme", "Clear current scheme?"):
            self.clear_scheme()
            
    def clear_scheme(self):
        for element in self.elements:
            # Delete all element components
            self.canvas.delete(element.rect)
            self.canvas.delete(element.text)
            if element.button_highlight:  # Delete button highlight if exists
                self.canvas.delete(element.button_highlight)
            for port in element.inputs:
                self.canvas.delete(port)
            if element.output:  # Check if output port exists
                self.canvas.delete(element.output)
        self.elements.clear()
        
        # Delete all connections
        for conn in self.connections:
            self.canvas.delete(conn[0])
        self.connections.clear()
        
        # Reset simulation mode if active
        if self.simulation_mode:
            self.toggle_simulation()
            
        # Reset status
        self.status_label.config(text="Ready")
        
    def save_scheme(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".lcs",
            filetypes=[("Logic Circuit Scheme", "*.lcs")]
        )
        if file_path:
            data = {
                "elements": [
                    {
                        "type": element.element_type,
                        "x": element.x,
                        "y": element.y
                    }
                    for element in self.elements
                ],
                "connections": [
                    {
                        "start": self.canvas.coords(conn[1]),
                        "end": self.canvas.coords(conn[2])
                    }
                    for conn in self.connections
                ]
            }
            with open(file_path, "w") as f:
                json.dump(data, f)
                
    def open_scheme(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Logic Circuit Scheme", "*.lcs")]
        )
        if file_path:
            self.clear_scheme()
            with open(file_path, "r") as f:
                data = json.load(f)
                # Restore elements and connections
                # Implementation needed
                
    def on_canvas_click(self, event):
        if self.simulation_mode:
            # Find clicked element
            clicked = self.canvas.find_closest(event.x, event.y)
            if not clicked:
                return
                
            # Check if clicked on an input element
            for element in self.elements:
                if element.element_type == "INPUT" and clicked[0] in [element.rect, element.text, element.button_highlight]:
                    # Toggle input value
                    element.value = not element.value
                    # Update button appearance
                    if element.value:
                        self.canvas.itemconfig(element.rect, fill="#e0e0e0")
                        self.canvas.itemconfig(element.button_highlight, outline="black")
                        self.canvas.itemconfig(element.output, fill="green")
                    else:
                        self.canvas.itemconfig(element.rect, fill="white")
                        self.canvas.itemconfig(element.button_highlight, outline="gray")
                        self.canvas.itemconfig(element.output, fill="gray")
                    # Update simulation
                    self.update_simulation()
                    return
            return
            
        # Normal mode - handle drag and drop and connections
        clicked = self.canvas.find_closest(event.x, event.y)
        if not clicked:
            return
            
        # Check if clicked on a port
        for element in self.elements:
            if clicked[0] in element.inputs + [element.output]:
                port_type = "output" if clicked[0] == element.output else "input"
                self.on_port_click(clicked[0], port_type)
                return
                
        # Check if clicked on an element for dragging
        for element in self.elements:
            if clicked[0] in [element.rect, element.text, element.button_highlight]:
                # Select element
                self.select_element(element)
                # Start dragging
                self.dragging_element = element
                self.drag_start_x = event.x - element.x
                self.drag_start_y = event.y - element.y
                return

    def select_element(self, element):
        # Deselect previous element if any
        if self.selected_element:
            self.canvas.itemconfig(self.selected_element.rect, outline="black")
        
        # Select new element
        self.selected_element = element
        self.canvas.itemconfig(element.rect, outline="blue", width=2)

    def delete_selected_element(self, event=None):
        if not self.selected_element:
            return
            
        # Delete all connections involving this element
        connections_to_delete = []
        for conn in self.connections:
            if (self.selected_element.output in [conn[1], conn[2]] or
                any(port in [conn[1], conn[2]] for port in self.selected_element.inputs)):
                connections_to_delete.append(conn[0])
        
        for line in connections_to_delete:
            self.delete_connection(line)
        
        # Delete element components
        self.canvas.delete(self.selected_element.rect)
        self.canvas.delete(self.selected_element.text)
        if self.selected_element.button_highlight:
            self.canvas.delete(self.selected_element.button_highlight)
        for port in self.selected_element.inputs:
            self.canvas.delete(port)
        if self.selected_element.output:
            self.canvas.delete(self.selected_element.output)
        
        # Remove element from list
        self.elements.remove(self.selected_element)
        self.selected_element = None
        
        # Update simulation if active
        if self.simulation_mode:
            self.update_simulation()

    def on_canvas_drag(self, event):
        if self.dragging_element:
            # Calculate new position
            new_x = event.x - self.drag_start_x
            new_y = event.y - self.drag_start_y
            
            # Calculate movement delta
            dx = new_x - self.dragging_element.x
            dy = new_y - self.dragging_element.y
            
            # Move element
            self.dragging_element.move(dx, dy)
            
            # Update connections
            self.update_connections()
            
    def on_canvas_release(self, event):
        self.dragging_element = None
        
    def update_connections(self):
        for conn in self.connections:
            start_coords = self.canvas.coords(conn[1])
            end_coords = self.canvas.coords(conn[2])
            self.canvas.coords(
                conn[0],
                (start_coords[0] + start_coords[2])/2,
                (start_coords[1] + start_coords[3])/2,
                (end_coords[0] + end_coords[2])/2,
                (end_coords[1] + end_coords[3])/2
            )
            # Update simulation if in simulation mode
            if self.simulation_mode:
                self.update_simulation()

    def on_canvas_right_click(self, event):
        # Find clicked item
        clicked = self.canvas.find_closest(event.x, event.y)
        if not clicked:
            return
            
        # Check if clicked on a connection line
        for conn in self.connections:
            if conn[0] == clicked[0]:
                self.delete_connection(conn[0])
                break

if __name__ == "__main__":
    root = tk.Tk()
    simulator = LogicCircuitSimulator(root)
    root.mainloop() 