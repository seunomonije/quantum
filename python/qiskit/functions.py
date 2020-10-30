import qiskit

# Functional imports
from qiskit import QuantumCircuit, execute, Aer, QuantumRegister, ClassicalRegister

# Noise Model imports
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, depolarizing_error

# Custom datatypes
from datatypes import CircuitResultPair

# Global variables
global backend
backend = Aer.get_backend('qasm_simulator')

"""
  Playground when going through IBM tutorial.
"""
def run_ancilla_circuit_playground():
  working_qubits = QuantumRegister(2, 'working_qubits')
  ancilla_qubit = QuantumRegister(1, 'ancilla_qubit')
  syndrome_bit = ClassicalRegister(1, 'syndrome_bit')

  # Construct circuit
  circuit = QuantumCircuit(working_qubits, ancilla_qubit, syndrome_bit)
  circuit.cx(working_qubits[0], ancilla_qubit[0])
  circuit.cx(working_qubits[1], ancilla_qubit[0])
  circuit.measure(ancilla_qubit, syndrome_bit)

  # Initialize working qubits in whichever state here.
  # In this case I'm flipping to the state |11>
  circuit_init = QuantumCircuit(working_qubits)
  circuit_init.x(working_qubits)

  result = execute(circuit_init+circuit, backend).result()
  counts = result.get_counts()

  return CircuitResultPair(circuit_init+circuit, counts)

"""
  Retrieves noise models from Qiskit to simulate a realistic environment.
  
  PARAMETERS:
    p_gate -> probability that an error occurs when applying a gate to our state
    p_meas -> probability that an error occurs in measurement
"""
def simulate_noise(p_gate, p_meas):
  
  # This is the bit-flip error channel
  # E(S) = (1-p)IroI + pXroX
  measurement_error = pauli_error([
    ('X', p_meas),
    ('I', 1 - p_meas)
  ])

  # Need to search documentation to see what's going on under the hood 
  error_gate1 = depolarizing_error(p_gate, 1)
  error_gate2 = error_gate1.tensor(error_gate1)
  
  noise_model = NoiseModel()
  # Apply bit flip error model to all measurements in the system
  noise_model.add_all_qubit_quantum_error(measurement_error, "measure")
  # Apply single qubit error model to all Pauli-X gates
  noise_model.add_all_qubit_quantum_error(error_gate1, ['x'])
  # Apply multi-qubit error model to all C-NOT gates
  noise_model.add_all_qubit_quantum_error(error_gate2, ['cx'])

  return noise_model
