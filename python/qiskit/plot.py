import pickle
import matplotlib.pyplot as plt

from qiskit.ignis.characterization.coherence import T1Fitter, T2StarFitter, T2Fitter
from qiskit.ignis.characterization.gates import AmpCalFitter, AngleCalFitter

"""
Plotting sandbox file
"""
def main():  
  # Store to file
  with open(f'results/dump.txt', 'rb') as file:
    results = pickle.load(file)

  qubits = [0, 2]
  t_q0 = 25.0

  plt.figure(figsize=(15,6))

  # t1_fit = T1Fitter(results.t1_circs_result, results.t1_xdata, qubits, fit_p0=[1, t_q0, 0], fit_bounds=([0, 0, -1], [2, 40, 1]))
  # print(t1_fit.time())
  # print(t1_fit.time_err())
  # print(t1_fit.params)
  # print(t1_fit.params_err)

  #t2_fit = T2Fitter(results.t2star_circs_result, results.t2star_xdata, qubits, fit_p0=[1, t_q0, 0], fit_bounds=([0, 0, -1], [2, 40, 1]))

  ampcal_fit = AngleCalFitter(results.anglecal_circs_result, results.anglecal_xdata, qubits, fit_p0=[1, t_q0, 0], fit_bounds=([0, 0, -1], [2, 40, 1]))
  for i in range(2):
    ax = plt.subplot(1, 2, i+1)
    ampcal_fit.plot(i, ax=ax)
  plt.show()
  return

if __name__ == '__main__':
  main()