import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import math
import tkinter as tk

class LogicalElement:
    def __init__(self, canvas, x, y, element_type):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.element_type = element_type
        self.inputs = []
        self.output = None
        self.value = False
        self.rect = None
        self.text = None
        self.button_highlight = None
        self.simulator = None  # Add reference to simulator
        self.create_visual()
        
    def set_simulator(self, simulator):
        self.simulator = simulator
        
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
        # Draw AND gate with rounded corners
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x+50, self.y+40,
            fill="#2b2b2b", outline="#404040", width=2
        )
        self.text = self.canvas.create_text(
            self.x+25, self.y+20,
            text="AND", fill="#ffffff", font=("Helvetica", 12, "bold")
        )
        
        # Create input ports
        self.inputs = [
            self.create_port(self.x, self.y+10, "input"),
            self.create_port(self.x, self.y+30, "input")
        ]
        # Create output port
        self.output = self.create_port(self.x+50, self.y+20, "output")
        
    def draw_or_gate(self):
        # Draw OR gate with rounded corners
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x+50, self.y+40,
            fill="#2b2b2b", outline="#404040", width=2
        )
        self.text = self.canvas.create_text(
            self.x+25, self.y+20,
            text="OR", fill="#ffffff", font=("Helvetica", 12, "bold")
        )
        
        # Create input ports
        self.inputs = [
            self.create_port(self.x, self.y+10, "input"),
            self.create_port(self.x, self.y+30, "input")
        ]
        # Create output port
        self.output = self.create_port(self.x+50, self.y+20, "output")
        
    def draw_not_gate(self):
        # Draw NOT gate with rounded corners
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x+50, self.y+40,
            fill="#2b2b2b", outline="#404040", width=2
        )
        self.text = self.canvas.create_text(
            self.x+25, self.y+20,
            text="NOT", fill="#ffffff", font=("Helvetica", 12, "bold")
        )
        
        # Create input port
        self.inputs = [self.create_port(self.x, self.y+20, "input")]
        # Create output port
        self.output = self.create_port(self.x+50, self.y+20, "output")
        
    def draw_xor_gate(self):
        # Draw XOR gate with rounded corners
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x+50, self.y+40,
            fill="#2b2b2b", outline="#404040", width=2
        )
        self.text = self.canvas.create_text(
            self.x+25, self.y+20,
            text="XOR", fill="#ffffff", font=("Helvetica", 12, "bold")
        )
        
        # Create input ports
        self.inputs = [
            self.create_port(self.x, self.y+10, "input"),
            self.create_port(self.x, self.y+30, "input")
        ]
        # Create output port
        self.output = self.create_port(self.x+50, self.y+20, "output")
        
    def draw_input_device(self):
        # Draw input device (button)
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x+50, self.y+40,
            fill="#2b2b2b", outline="#404040", width=2
        )
        self.text = self.canvas.create_text(
            self.x+25, self.y+20,
            text="IN", fill="#ffffff", font=("Helvetica", 12, "bold")
        )
        
        # Create output port
        self.output = self.create_port(self.x+50, self.y+20, "output")
        
        # Add button-like appearance
        self.button_highlight = self.canvas.create_rectangle(
            self.x+2, self.y+2, self.x+48, self.y+38,
            fill="", outline="#505050", width=1
        )
        
    def draw_output_device(self):
        # Draw LED symbol (circle with input)
        self.rect = self.canvas.create_oval(
            self.x, self.y, self.x+40, self.y+40,
            fill="#2b2b2b", outline="#404040", width=2
        )
        self.text = self.canvas.create_text(
            self.x+20, self.y+20,
            text="LED", fill="#ffffff", font=("Helvetica", 12, "bold")
        )
        
        # Create input port
        self.inputs = [self.create_port(self.x, self.y+20, "input")]
        
    def create_port(self, x, y, port_type):
        port = self.canvas.create_oval(
            x-5, y-5, x+5, y+5,
            fill="#404040", outline="#505050", width=1
        )
        # Bind click event directly to simulator's on_port_click
        self.canvas.tag_bind(port, "<Button-1>", 
                           lambda e, p=port, t=port_type: self.simulator.on_port_click(p, t))
        return port

    def move(self, dx, dy):
        # Update element position
        self.x += dx
        self.y += dy
        
        # Move all visual elements
        if self.rect:
            self.canvas.move(self.rect, dx, dy)
        if self.text:
            self.canvas.move(self.text, dx, dy)
        if self.button_highlight:
            self.canvas.move(self.button_highlight, dx, dy)
            
        # Move input ports
        for port in self.inputs:
            self.canvas.move(port, dx, dy)
            
        # Move output port
        if self.output:
            self.canvas.move(self.output, dx, dy)

class LogicCircuitSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Logic Circuit Simulator")
        self.geometry("1200x800")
        
        # Set initial theme to dark
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main frames
        self.create_toolbar()
        self.create_canvas()
        self.create_sidebar()
        
        # Initialize variables
        self.elements = []
        self.connections = []
        self.selected_port = None
        self.dragging_element = None
        self.simulation_mode = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.selected_element = None
        self.current_theme = "dark"  # Add theme tracking
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        self.bind("<Delete>", self.delete_selected_element)
        
    def create_toolbar(self):
        self.toolbar = ctk.CTkFrame(self, height=40)
        self.toolbar.pack(fill="x", padx=5, pady=5)
        
        # File operations
        ctk.CTkButton(self.toolbar, text="New", command=self.new_scheme).pack(side="left", padx=5)
        ctk.CTkButton(self.toolbar, text="Open", command=self.open_scheme).pack(side="left", padx=5)
        ctk.CTkButton(self.toolbar, text="Save", command=self.save_scheme).pack(side="left", padx=5)
        
        # Simulation controls
        self.sim_button = ctk.CTkButton(
            self.toolbar, text="Start Simulation",
            command=self.toggle_simulation
        )
        self.sim_button.pack(side="left", padx=5)
        
        # Theme toggle
        self.theme_button = ctk.CTkButton(
            self.toolbar, text="Toggle Theme",
            command=self.toggle_theme
        )
        self.theme_button.pack(side="left", padx=5)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.toolbar, text="Ready",
            font=("Helvetica", 12)
        )
        self.status_label.pack(side="right", padx=5)
        
    def create_canvas(self):
        # Create canvas with scrollbars
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        
        # Use regular tkinter Canvas instead of CTkCanvas
        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg="#1a1a1a",
            width=800,
            height=600,
            highlightthickness=0
        )
        
        self.v_scroll = ctk.CTkScrollbar(
            self.canvas_frame,
            orientation="vertical",
            command=self.canvas.yview
        )
        self.h_scroll = ctk.CTkScrollbar(
            self.canvas_frame,
            orientation="horizontal",
            command=self.canvas.xview
        )
        
        self.canvas.configure(
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set
        )
        
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="right", fill="y", padx=5, pady=5)
        
        # Add element buttons
        ctk.CTkLabel(
            self.sidebar,
            text="Elements",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # Create buttons with consistent styling
        button_style = {
            "font": ("Helvetica", 12),
            "height": 35,
            "corner_radius": 8
        }
        
        ctk.CTkButton(
            self.sidebar,
            text="Input",
            command=lambda: self.create_element("INPUT"),
            **button_style
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            self.sidebar,
            text="Output (LED)",
            command=lambda: self.create_element("OUTPUT"),
            **button_style
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            self.sidebar,
            text="AND Gate",
            command=lambda: self.create_element("AND"),
            **button_style
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            self.sidebar,
            text="OR Gate",
            command=lambda: self.create_element("OR"),
            **button_style
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            self.sidebar,
            text="NOT Gate",
            command=lambda: self.create_element("NOT"),
            **button_style
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            self.sidebar,
            text="XOR Gate",
            command=lambda: self.create_element("XOR"),
            **button_style
        ).pack(fill="x", padx=10, pady=5)
        
        # Add clear button
        ctk.CTkButton(
            self.sidebar,
            text="Clear All",
            command=self.clear_scheme,
            fg_color="#ff4444",
            hover_color="#cc0000",
            **button_style
        ).pack(fill="x", padx=10, pady=20)
        
    def toggle_theme(self):
        # Toggle between dark and light themes
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        ctk.set_appearance_mode(self.current_theme)
        
        # Update canvas background
        bg_color = "#f0f0f0" if self.current_theme == "light" else "#1a1a1a"
        self.canvas.configure(bg=bg_color)
        
        # Update element colors
        for element in self.elements:
            if element.element_type == "OUTPUT":
                if element.value:
                    self.canvas.itemconfig(element.rect, fill="red", outline="red")
                    self.canvas.itemconfig(element.text, fill="white")
                else:
                    self.canvas.itemconfig(element.rect, fill="#ffffff" if self.current_theme == "light" else "#2b2b2b", 
                                         outline="#808080" if self.current_theme == "light" else "#404040")
                    self.canvas.itemconfig(element.text, fill="#000000" if self.current_theme == "light" else "#ffffff")
            else:
                # For logic elements
                element_bg = "#ffffff" if self.current_theme == "light" else "#2b2b2b"
                element_outline = "#808080" if self.current_theme == "light" else "#404040"
                text_color = "#000000" if self.current_theme == "light" else "#ffffff"
                
                self.canvas.itemconfig(element.rect, fill=element_bg, outline=element_outline)
                self.canvas.itemconfig(element.text, fill=text_color)
                
                # Update ports
                port_fill = "#a0a0a0" if self.current_theme == "light" else "#404040"
                port_outline = "#808080" if self.current_theme == "light" else "#505050"
                
                for port in element.inputs:
                    self.canvas.itemconfig(port, fill=port_fill, outline=port_outline)
                if element.output:
                    if element.value:
                        self.canvas.itemconfig(element.output, fill="#00ff00")
                    else:
                        self.canvas.itemconfig(element.output, fill=port_fill, outline=port_outline)
                
                # Update button highlight for input elements
                if element.element_type == "INPUT" and element.button_highlight:
                    highlight_color = "#c0c0c0" if self.current_theme == "light" else "#505050"
                    self.canvas.itemconfig(element.button_highlight, outline=highlight_color)
        
        # Update connections - white in dark theme, black in light theme
        connection_color = "#000000" if self.current_theme == "light" else "#ffffff"
        for conn in self.connections:
            self.canvas.itemconfig(conn[0], fill=connection_color, width=2)
        
    def create_element(self, element_type):
        element = LogicalElement(self.canvas, 50, 50, element_type)
        element.set_simulator(self)
        self.elements.append(element)
        
    def on_port_click(self, port, port_type):
        print(f"Port click: type={port_type}")  # Debug print
        
        if self.simulation_mode:
            if port_type == "input":
                element = self.find_element_by_port(port)
                if element and element.element_type == "INPUT":
                    element.value = not element.value
                    if element.value:
                        self.canvas.itemconfig(element.rect, fill="#404040")
                        self.canvas.itemconfig(element.button_highlight, outline="#606060")
                        self.canvas.itemconfig(element.output, fill="#00ff00")
                    else:
                        self.canvas.itemconfig(element.rect, fill="#2b2b2b")
                        self.canvas.itemconfig(element.button_highlight, outline="#404040")
                        self.canvas.itemconfig(element.output, fill="#404040")
                    self.update_simulation()
            return
            
        if self.selected_port is None:
            print("First port selected")  # Debug print
            self.selected_port = (port, port_type)
            self.canvas.itemconfig(port, fill="#00ff00")
            self.status_label.configure(text="Select second port")
        else:
            print("Second port selected")  # Debug print
            if self.selected_port[0] == port:
                # Deselect if clicking the same port
                self.canvas.itemconfig(port, fill="#404040")
                self.selected_port = None
                self.status_label.configure(text="Ready")
                return
                
            # Create connection
            if self.is_valid_connection(self.selected_port[1], port_type):
                print("Creating connection")  # Debug print
                self.create_connection(self.selected_port[0], port)
                self.status_label.configure(text="Connection created")
            else:
                print("Invalid connection")  # Debug print
                self.status_label.configure(text="Invalid connection")
                
            # Reset selection
            self.canvas.itemconfig(self.selected_port[0], fill="#404040")
            self.selected_port = None
            self.status_label.configure(text="Ready")

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
            print("Starting connection creation")  # Debug print
            # Get coordinates
            start_coords = self.canvas.coords(start_port)
            end_coords = self.canvas.coords(end_port)
            
            print(f"Start coords: {start_coords}")  # Debug print
            print(f"End coords: {end_coords}")  # Debug print
            
            if not start_coords or not end_coords:
                print("Invalid coordinates")  # Debug print
                self.status_label.configure(text="Error: Invalid port coordinates")
                return
                
            # Calculate center points of the ports
            start_x = (start_coords[0] + start_coords[2]) / 2
            start_y = (start_coords[1] + start_coords[3]) / 2
            end_x = (end_coords[0] + end_coords[2]) / 2
            end_y = (end_coords[1] + end_coords[3]) / 2
            
            # Create line
            line = self.canvas.create_line(
                start_x, start_y,
                end_x, end_y,
                fill="#ffffff", width=2,
                tags=("connection",)  # Add tag for easier identification
            )
            print(f"Line created: {line}")  # Debug print
            
            # Bind right-click event to delete connection
            self.canvas.tag_bind(line, "<Button-3>", lambda e: self.delete_connection(line))
            
            # Store connection
            self.connections.append((line, start_port, end_port))
            print(f"Connection stored. Total connections: {len(self.connections)}")  # Debug print
            
            # Update simulation if in simulation mode
            if self.simulation_mode:
                self.update_simulation()
                
            self.status_label.configure(text="Connection created")
        except Exception as e:
            print(f"Error in create_connection: {str(e)}")  # Debug print
            self.status_label.configure(text=f"Error creating connection: {str(e)}")
            # Reset selection
            if self.selected_port:
                self.canvas.itemconfig(self.selected_port[0], fill="#404040")
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
            self.sim_button.configure(text="Stop Simulation")
            self.status_label.configure(text="Simulation mode - Click on input elements to toggle")
            
            for element in self.elements:
                if element.element_type == "INPUT":
                    element.value = False
                    self.canvas.itemconfig(element.rect, fill="#2b2b2b")
                    self.canvas.itemconfig(element.button_highlight, outline="#404040")
                    self.canvas.itemconfig(element.output, fill="#404040")
                elif element.element_type == "OUTPUT":
                    self.canvas.itemconfig(element.rect, fill="#2b2b2b")
                else:
                    self.canvas.itemconfig(element.output, fill="#404040")
                    
            self.update_simulation()
        else:
            self.sim_button.configure(text="Start Simulation")
            self.status_label.configure(text="Ready")
            
    def update_simulation(self):
        if not self.simulation_mode:
            return

        # Create dictionary for storing input values of each element
        input_values = {element: [] for element in self.elements}
        
        # Create dictionary for storing output values of each element
        output_values = {element: element.value for element in self.elements}

        # Collect all input values for each element
        for conn in self.connections:
            start_port = conn[1]
            end_port = conn[2]
            
            # Find elements connected through these ports
            start_element = None
            end_element = None
            
            for element in self.elements:
                if start_port == element.output:
                    start_element = element
                if end_port in element.inputs:
                    end_element = element
                    
            if start_element and end_element:
                input_values[end_element].append(output_values[start_element])

        # Process each element
        for element in self.elements:
            if element.element_type == "INPUT":
                continue  # Skip input elements, their values are already set

            # Get input values for the element
            inputs = input_values[element]
            
            # Calculate output value based on element type
            if element.element_type == "AND":
                element.value = all(inputs) if inputs else False
            elif element.element_type == "OR":
                element.value = any(inputs) if inputs else False
            elif element.element_type == "NOT":
                element.value = not inputs[0] if inputs else False
            elif element.element_type == "XOR":
                element.value = sum(inputs) % 2 == 1 if inputs else False
            elif element.element_type == "OUTPUT":
                # For LED, take value from input
                if inputs:
                    element.value = inputs[0]
                else:
                    element.value = False

            # Update output value in dictionary
            output_values[element] = element.value

            # Update visual state of element
            if element.element_type == "OUTPUT":
                if element.value:
                    # If input is 1 - LED is red
                    self.canvas.itemconfig(element.rect, fill="red", outline="red")
                    self.canvas.itemconfig(element.text, fill="white")
                else:
                    # If input is 0 - LED is white
                    self.canvas.itemconfig(element.rect, fill="#2b2b2b", outline="#404040")
                    self.canvas.itemconfig(element.text, fill="#ffffff")
            else:
                # For logic elements, update output port color
                color = "#00ff00" if element.value else "#404040"
                self.canvas.itemconfig(element.output, fill=color)

    def new_scheme(self):
        if messagebox.askyesno("New Scheme", "Clear current scheme?"):
            self.clear_scheme()
            
    def clear_scheme(self):
        for element in self.elements:
            self.canvas.delete(element.rect)
            self.canvas.delete(element.text)
            if element.button_highlight:
                self.canvas.delete(element.button_highlight)
            for port in element.inputs:
                self.canvas.delete(port)
            if element.output:
                self.canvas.delete(element.output)
        self.elements.clear()
        
        for conn in self.connections:
            self.canvas.delete(conn[0])
        self.connections.clear()
        
        if self.simulation_mode:
            self.toggle_simulation()
            
        self.status_label.configure(text="Ready")
        
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
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    
                    # Create elements
                    for element_data in data["elements"]:
                        element = LogicalElement(
                            self.canvas,
                            element_data["x"],
                            element_data["y"],
                            element_data["type"]
                        )
                        element.set_simulator(self)
                        self.elements.append(element)
                    
                    # Create connections
                    for conn_data in data["connections"]:
                        start_coords = conn_data["start"]
                        end_coords = conn_data["end"]
                        
                        # Find closest ports
                        start_port = self.find_closest_port(start_coords[0], start_coords[1])
                        end_port = self.find_closest_port(end_coords[0], end_coords[1])
                        
                        if start_port and end_port:
                            self.create_connection(start_port, end_port)
                            
                self.status_label.configure(text="Scheme loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load scheme: {str(e)}")
                self.status_label.configure(text="Error loading scheme")
                
    def find_closest_port(self, x, y):
        closest_port = None
        min_distance = float('inf')
        
        for element in self.elements:
            # Check output port
            if element.output:
                port_coords = self.canvas.coords(element.output)
                if port_coords:
                    port_x = (port_coords[0] + port_coords[2]) / 2
                    port_y = (port_coords[1] + port_coords[3]) / 2
                    distance = ((port_x - x) ** 2 + (port_y - y) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        closest_port = element.output
            
            # Check input ports
            for port in element.inputs:
                port_coords = self.canvas.coords(port)
                if port_coords:
                    port_x = (port_coords[0] + port_coords[2]) / 2
                    port_y = (port_coords[1] + port_coords[3]) / 2
                    distance = ((port_x - x) ** 2 + (port_y - y) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        closest_port = port
        
        return closest_port if min_distance < 20 else None  # Return port if within 20 pixels

    def on_canvas_click(self, event):
        if self.simulation_mode:
            clicked = self.canvas.find_closest(event.x, event.y)
            if not clicked:
                return
                
            for element in self.elements:
                if element.element_type == "INPUT" and clicked[0] in [element.rect, element.text, element.button_highlight]:
                    element.value = not element.value
                    if element.value:
                        self.canvas.itemconfig(element.rect, fill="#404040")
                        self.canvas.itemconfig(element.button_highlight, outline="#606060")
                        self.canvas.itemconfig(element.output, fill="#00ff00")
                    else:
                        self.canvas.itemconfig(element.rect, fill="#2b2b2b")
                        self.canvas.itemconfig(element.button_highlight, outline="#404040")
                        self.canvas.itemconfig(element.output, fill="#404040")
                    self.update_simulation()
                    return
            return
            
        clicked = self.canvas.find_closest(event.x, event.y)
        if not clicked:
            return
            
        for element in self.elements:
            if clicked[0] in element.inputs + [element.output]:
                port_type = "output" if clicked[0] == element.output else "input"
                self.on_port_click(clicked[0], port_type)
                return
                
        for element in self.elements:
            if clicked[0] in [element.rect, element.text, element.button_highlight]:
                self.select_element(element)
                self.dragging_element = element
                self.drag_start_x = event.x - element.x
                self.drag_start_y = event.y - element.y
                return

    def select_element(self, element):
        if self.selected_element:
            self.canvas.itemconfig(self.selected_element.rect, outline="#404040", width=2)
        
        self.selected_element = element
        self.canvas.itemconfig(element.rect, outline="#00aaff", width=2)

    def delete_selected_element(self, event=None):
        if not self.selected_element:
            return
            
        connections_to_delete = []
        for conn in self.connections:
            if (self.selected_element.output in [conn[1], conn[2]] or
                any(port in [conn[1], conn[2]] for port in self.selected_element.inputs)):
                connections_to_delete.append(conn[0])
        
        for line in connections_to_delete:
            self.delete_connection(line)
        
        self.canvas.delete(self.selected_element.rect)
        self.canvas.delete(self.selected_element.text)
        if self.selected_element.button_highlight:
            self.canvas.delete(self.selected_element.button_highlight)
        for port in self.selected_element.inputs:
            self.canvas.delete(port)
        if self.selected_element.output:
            self.canvas.delete(self.selected_element.output)
        
        self.elements.remove(self.selected_element)
        self.selected_element = None
        
        if self.simulation_mode:
            self.update_simulation()

    def on_canvas_drag(self, event):
        if self.dragging_element:
            new_x = event.x - self.drag_start_x
            new_y = event.y - self.drag_start_y
            
            dx = new_x - self.dragging_element.x
            dy = new_y - self.dragging_element.y
            
            self.dragging_element.move(dx, dy)
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
        clicked = self.canvas.find_closest(event.x, event.y)
        if not clicked:
            return
            
        for conn in self.connections:
            if conn[0] == clicked[0]:
                self.delete_connection(conn[0])
                break

if __name__ == "__main__":
    app = LogicCircuitSimulator()
    app.mainloop() 