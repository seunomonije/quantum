import cirq
from cirq.circuits import InsertStrategy
import numpy as np
import matplotlib 
import random 
import socket
import select
import time
import pickle

# HELPER FUNCTIONS

def bitstring(bits):
    return ''.join('1' if e else '0' for e in bits)

def entangle(current, target, circuit):
    circuit.append([
        cirq.H(current),
        cirq.CNOT(current, target)
    ])
    
def superdenseCoding():
    qreg = [cirq.LineQubit(x) for x in range(2)]
    circuit = cirq.Circuit()

    # operations dictionary for each message
    message = {
        "00" : [],
        "01" : [cirq.X(qreg[0])],
        "10" : [cirq.Z(qreg[0])],
        "11" : [cirq.X(qreg[0]), cirq.Z(qreg[0])]
    }

    # Alice creates a bell pair
    circuit.append(cirq.H(qreg[0]))
    circuit.append(cirq.CNOT(qreg[0], qreg[1]))

    # Choose a random message to send to bob
    msgChosenByAlice = random.choice(list(message.keys()))
    print("Alice's sent message =", msgChosenByAlice)

    # Encode the message with the requested operation
    circuit.append(message[msgChosenByAlice])

    # Bob applies the CNOT then the Hadamard gate
    circuit.append(cirq.CNOT(qreg[0], qreg[1]))
    circuit.append(cirq.H(qreg[0]))

    # Then Bob decides to measure, insert strategy inline just for circuit clarity
    circuit.append([cirq.measure(qreg[0]), cirq.measure(qreg[1])], strategy = InsertStrategy.INLINE)

    print("\nCircuit:")
    print(circuit)

    sim = cirq.Simulator()
    res = sim.run(circuit, repetitions=1)

    print("\nBob's received message=", bitstring(res.measurements.values()))

def entangle2Qubits(xVal, yVal):
    ######## ENTANGLEMENT ########
    msg = cirq.LineQubit(0)

    # Pauli gates, rotate the state around the associated axis with by one (val)-turn
    ranq = cirq.X(msg)**xVal, cirq.Y(msg)**yVal

    circuit = cirq.Circuit()
    circuit.append(ranq)

    sim = cirq.Simulator()
    original_message = sim.simulate(circuit)

    expected = cirq.bloch_vector_from_state_vector(original_message.final_state, 0)

    print("expected x: ", expected[0], 
        "expected y: ", expected[1], 
        "expected z: ", expected[2],
        "\n")

    alice, bob = cirq.LineQubit.range(1, 3)
    circuit.append([cirq.H(alice), cirq.CNOT(alice, bob)])
    circuit.append([cirq.CNOT(msg, alice), cirq.H(msg)])
    circuit.append(cirq.measure(msg, alice))
    circuit.append([cirq.CNOT(alice, bob), cirq.CZ(msg, bob)])
    print(circuit)

    print("\n final results:")
    final_results = sim.simulate(circuit)

    teleported = cirq.bloch_vector_from_state_vector(final_results.final_state, 2)
    print("x: ", teleported[0], 
        "y: ", teleported[1], 
        "z: ", teleported[2])
    
    ## can just return teleported because we expect teleported and expected to be the same
    return teleported

def bellInequalityTest():

    alice = cirq.GridQubit(0,0)
    bob = cirq.GridQubit(1,0)
    alice_referee = cirq.GridQubit(0,1)
    bob_referee = cirq.GridQubit(1,1)

    circuit = cirq.Circuit()

    entangle(alice, bob, circuit)

    # Add this pauli-x gate, not sure why book doesn't say
    circuit.append(cirq.X(alice)**-0.25)

    # Referee generates random bit, which Alice and bob will read
    circuit.append([
        cirq.H(alice_referee),
        cirq.H(bob_referee)
    ], strategy=InsertStrategy.INLINE)

    # Alice and Bob do sqrt(X) gate based on the refs values
    circuit.append([
        cirq.CNOT(alice_referee, alice)**0.5,
        cirq.CNOT(bob_referee, bob)**0.5
    ])

    # Measure the results
    circuit.append([
        cirq.measure(alice, key='a'),
        cirq.measure(bob, key='b'),
        cirq.measure(alice_referee, key='x'),
        cirq.measure(bob_referee, key='y'),
    ],  strategy = InsertStrategy.INLINE)

    print("\nCircuit:")
    print(circuit)

    print()
    repetitions = 1000
    print('Simulation {} repetitions...'.format(repetitions))
    result = cirq.Simulator().run(program=circuit, repetitions=repetitions)

    # Result collection
    a = np.array(result.measurements['a'][:, 0])
    b = np.array(result.measurements['b'][:, 0])
    x = np.array(result.measurements['x'][:, 0])
    y = np.array(result.measurements['y'][:, 0])

    # Get winning percentage
    outcomes = a ^ b == x & y
    win_percent = len([e for e in outcomes if e]) * 100 / repetitions

    # Print data
    print('\nResults')
    print('a:', bitstring(a))
    print('b:', bitstring(b))
    print('x:', bitstring(x))
    print('y:', bitstring(y))
    print('(a XOR b) == (x AND y):\n', bitstring(outcomes))
    print('Win rate: {}%'.format(win_percent))

def deutchAlgorithmOperations(qubit1, qubit2, oracle):
    yield cirq.X(qubit1)
    yield cirq.H(qubit1), cirq.H(qubit2)
    yield oracle
    yield cirq.H(qubit1)
    yield cirq.measure(qubit1)

def deutschAlgorithm():
    q0, q1 = cirq.LineQubit.range(2)

    oracles = {
        '0' : [],
        '1' : [cirq.X(q1)],
        'X' : [cirq.CNOT(q0, q1)],
        'NOTX' : [cirq.CNOT(q0, q1), cirq.X(q1)]
    }

    # Display the circuits
    for key, oracle in oracles.items():
        print('Circuit for {}...'.format(key))
        print(cirq.Circuit.from_ops(deutchAlgorithmOperations(q0, q1, oracle)), end="\n\n")
    
    simulator = cirq.Simulator()

    # Execute the circuit for each oracle
    for key,oracle in oracles.items():
        result = simulator.run(
            cirq.Circuit.from_ops(deutchAlgorithmOperations(q0, q1, oracle)),
            repetitions = 10
        )
        print('oracle: {:<4} results: {}'.format(key,result))
