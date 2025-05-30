import copy

class Gate:
    def __init__(self, inputs=2, output=1, gate_type='and'):
        self.inputs = inputs
        self.output = output
        self.gate_type = gate_type
        self.connections = {}

    def add_connection(self, input_id, output_gate, output_id):
        if input_id in self.connections:
            raise ValueError("Input {} is already connected.".format(input_id))
        self.connections[input_id] = (output_gate, output_id)

    def remove_connection(self, input_id):
        if input_id not in self.connections:
            raise ValueError("Input {} is not connected.".format(input_id))
        del self.connections[input_id]

    def process(self):
        output_value = 0
        for input_id, (output_gate, output_id) in self.connections.items():
            output_value += output_gate.connections[output_id][0].output
        if self.gate_type == 'and':
            return int(output_value > 0)
        elif self.gate_type == 'or':
            return int(output_value >= 1)
        elif self.gate_type == 'xor':
            return int(output_value == 1)
        else:
            raise ValueError("Invalid gate type: {}".format(self.gate_type))

def create_gates():
    and_gate = Gate(2, 1, 'and')
    or_gate = Gate(2, 1, 'or')
    xor_gate = Gate(2, 1, 'xor')

    and_gate.add_connection(0, xor_gate, 0)
    and_gate.add_connection(1, or_gate, 1)

    or_gate.add_connection(0, and_gate, 0)
    or_gate.add_connection(1, xor_gate, 1)

    xor_gate.add_connection(0, or_gate, 0)
    xor_gate.add_connection(1, and_gate, 1) # corrected line

    return and_gate, or_gate, xor_gate

def main():
    and_gate, or_gate, xor_gate = create_gates()

    and_gate.process()
    or_gate.process()
    xor_gate.process()

    print("AND gate output:", and_gate.output)
    print("OR gate output:", or_gate.output)
    print("XOR gate output:", xor_gate.output)

if __name__ == "__main__":
    main()