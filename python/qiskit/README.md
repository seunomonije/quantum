## Qiskit Implementations

### Currently includes:
  - Ability to gather qubit decoherence data from IBM open systems or your own simulated backends.

### Tutorials:

#### General Notes
  - Build the project using `make`, and then run the contents of main.py by using `./scripts/main.py`
  - You will need to use your own API key in order to access IBM's real quantum computers. You can sign up for an account at https://quantum-computing.ibm.com/
    - Create a file in `secrets/APIKey.txt` and insert your API key locally. This repository will protect the key from being accidentally pushed to the web. Refer to the first few lines of main.py and scripts/run.sh to see how the API key is retrieved for stdin.
  - Pre-loaded data from IBM's `ibmq-athens` system can be found in the results folder. You can load this data and play with it by using pickle.
  - Please raise attention to any bugs by opening up a Github Issue.
  
#### Read Qubit Decoherence in a system
  - Look at at classes.py and main.py for implementation on how to gather qubit decoherence data.
