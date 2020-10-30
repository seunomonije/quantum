# importing entire package might take a while and may be unnecessary.
# Potential speedup here.
import qiskit
from qiskit import QuantumCircuit, execute, Aer, QuantumRegister, ClassicalRegister
from functions import simulate_noise, run_ancilla_circuit_playground

def main():
  global backend
  backend = Aer.get_backend('qasm_simulator')

  noise_model = simulate_noise(.5, .5)

  # 3 qubit, 3 classical bit circuit
  circuit = QuantumCircuit(3, 3, name="initial")
  
  # Measure each qubit
  circuit_reg_quantum = circuit.qregs
  circuit_reg_classical = circuit.cregs

  circuit.measure(circuit_reg_quantum[0], circuit_reg_classical[0])

  # 1024 shots is default
  result = execute(circuit, backend, noise_model=noise_model).result()
  counts = result.get_counts()

  playgroundResults = run_ancilla_circuit_playground()
  print(playgroundResults.circuit)
  print(playgroundResults.result)
  return

if __name__ == "__main__":
  main()
