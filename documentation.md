# Logic Circuit Simulator - Technical Documentation

## Overview
The Logic Circuit Simulator is a Python-based application that allows users to create, simulate, and save digital logic circuits using a graphical interface. Built with CustomTkinter, it provides an intuitive way to design and test logic circuits with various gates and components.

## Technical Stack

### Core Technologies
- **Python 3.x**: Primary programming language
- **CustomTkinter**: Modern UI framework for Tkinter
- **Tkinter**: Standard Python GUI toolkit
- **JSON**: Data serialization for circuit schemas

### Key Dependencies
- **customtkinter**: Enhanced Tkinter widgets with modern styling
- **tkinter**: Base GUI framework
- **json**: Standard library for JSON handling
- **math**: Standard library for mathematical operations

### Development Tools
- **Git**: Version control system
- **Markdown**: Documentation format
- **JSON**: Configuration and data storage format

### Architecture
- **MVC-like Pattern**: Separation of UI (View) and logic (Model)
- **Event-Driven Architecture**: Based on Tkinter's event system
- **Object-Oriented Design**: Class-based component system

## Core Components

### LogicalElement Class
The `LogicalElement` class represents individual components in the circuit.

#### Properties
- `canvas`: Reference to the Tkinter canvas
- `x, y`: Position coordinates
- `element_type`: Type of the element ("AND", "OR", "NOT", "XOR", "INPUT", "OUTPUT")
- `inputs`: List of input ports
- `output`: Output port
- `value`: Current logical state (True/False)
- `rect`: Visual rectangle representation
- `text`: Text label
- `button_highlight`: Visual highlight for input elements
- `simulator`: Reference to the main simulator instance

#### Methods
- `create_visual()`: Creates the visual representation based on element type
- `draw_and_gate()`, `draw_or_gate()`, `draw_not_gate()`, `draw_xor_gate()`: Draw specific gate types
- `draw_input_device()`, `draw_output_device()`: Draw input/output components
- `create_port(x, y, port_type)`: Creates connection ports
- `move(dx, dy)`: Handles element movement

### LogicCircuitSimulator Class
The main application class that manages the circuit simulation.

#### Properties
- `elements`: List of all circuit elements
- `connections`: List of all wire connections
- `selected_port`: Currently selected port for connection
- `dragging_element`: Element being moved
- `simulation_mode`: Current simulation state
- `selected_element`: Currently selected element
- `current_theme`: Current UI theme

#### Key Methods

##### Circuit Management
- `create_element(element_type)`: Creates new circuit elements
- `create_connection(start_port, end_port)`: Creates wire connections
- `delete_connection(line)`: Removes wire connections
- `update_connections()`: Updates wire positions during movement

##### Simulation
- `toggle_simulation()`: Toggles simulation mode
- `update_simulation()`: Updates circuit state based on connections
- `find_element_by_port(port)`: Locates elements by port reference

##### File Operations
- `save_scheme()`: Saves circuit to .lcs file
- `open_scheme()`: Loads circuit from .lcs file
- `clear_scheme()`: Resets the circuit

##### UI Management
- `toggle_theme()`: Switches between light and dark themes
- `create_toolbar()`: Creates the main toolbar
- `create_canvas()`: Sets up the drawing canvas
- `create_sidebar()`: Creates the element selection sidebar

## Circuit Elements

### Available Components
1. **Input Device**
   - Single output port
   - Toggleable state in simulation mode

2. **Output Device (LED)**
   - Single input port
   - Visual feedback (red when active)

3. **Logic Gates**
   - AND Gate: Two inputs, one output
   - OR Gate: Two inputs, one output
   - NOT Gate: One input, one output
   - XOR Gate: Two inputs, one output

### Connection Rules
- Output ports can only connect to input ports
- Input ports can only connect to output ports
- Multiple connections can be made to input ports
- Each output port can connect to multiple inputs

## File Format (.lcs)
The simulator uses a JSON-based file format to save and load circuits:

```json
{
    "elements": [
        {
            "type": "element_type",
            "x": x_coordinate,
            "y": y_coordinate
        }
    ],
    "connections": [
        {
            "start": [x1, y1, x2, y2],
            "end": [x1, y1, x2, y2]
        }
    ]
}
```

## User Interactions

### Mouse Controls
- **Left Click**: Select elements, create connections
- **Right Click**: Delete connections
- **Drag**: Move elements
- **Delete Key**: Remove selected element

### Simulation Mode
- Toggle simulation with "Start Simulation" button
- Click input elements to change their state
- Visual feedback shows signal propagation

## Theme Support
The simulator supports both light and dark themes:
- Dark theme: Dark backgrounds with light text
- Light theme: Light backgrounds with dark text
- Automatic color adjustments for all elements

## Error Handling
- Connection validation
- File operation error handling
- Invalid state prevention
- Graceful error recovery

## Performance Considerations
- Efficient connection updates
- Optimized simulation calculations
- Smooth element movement
- Responsive UI updates 