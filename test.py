import pulser
import numpy as np
from pprint import pprint
from pulser import Pulse, Sequence, Register
from pulser.devices import Chadoq2, MockDevice
from pulser.waveforms import RampWaveform, BlackmanWaveform
from pulser_simulation import QutipEmulator
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist


# def find_MIS(coordinates, max_dist):
#     # Convert the coordinates to a dictionary
#     qubit_dict = {f'q{i}': coord for i, coord in enumerate(coordinates)}

#     reg = Register(qubit_dict)
#     #reg.draw(with_labels=True)

#     # Create a Sequence with the Register
#     seq = Sequence(reg, device=Chadoq2)

#     # Declare a channel with a specific Rydberg blockade radius
#     rydberg_radius = max_dist
#     seq.declare_channel('ryd', 'rydberg_global', initial_target=rydberg_radius)
    
#     # # Define the Rabi frequency (amplitude)
#     # omega = 2 * np.pi * 1  # 1 rad/µs for example, but you can adjust this
#     # duration = int(np.pi / omega)
#     # # Create a constant waveform for detuning with value 0 and the desired duration
#     # detuning_wf = Waveform(duration, np.zeros(duration))

#     # Define the π-pulse
#     #pi_pulse = Pulse.ConstantDetuning(Pulse.ConstantAmplitude(omega, detuning_wf, 0), 0, duration)
#     duration = 1000  # Typical: ~1 µsec
#     pi_pulse = Pulse.ConstantDetuning(BlackmanWaveform(duration, np.pi), 0.0, 0.0)

    
#     # Add the pulse to the channel to turn qubits from |0⟩ to |1⟩
#     seq.add(pi_pulse, 'ryd')
    
#     # Simulate the sequence
#     sim = QutipEmulator.from_sequence(seq)
#     res = sim.run()  # Returns a SimulationResults instance

#     r = [1, 0]
#     rr = [1, 0]
#     for i in range(len(coordinates)-1):
#         rr = np.kron(r, rr)
#     occup = [np.outer(rr, np.conj(rr))]
#     data = res.expect(occup)[0]  # Get expectation value for the occupation operator
    
    
#     # Extract the coordinates from the register
#     coords = list(reg.qubits.values())
#     # Compute pairwise distances
#     distances = pdist(coords)
    
#     for i, R in enumerate(distances):
#         plt.plot(data[i], label=f"R={R}")
#         plt.xlabel("Time (ns)", fontsize=14)
#         plt.ylabel(r"Occupation of $|rr\rangle$", fontsize=14)
#         plt.legend()
#     plt.show()
    
#     return data

def find_MIS(coordinates, max_dist):
    reg = Register.from_coordinates(coordinates, prefix="")
    reg.draw(blockade_radius=max_dist, draw_half_radius=True, draw_graph=True)

    


#Example

antenna_1 = (0, 0)
antenna_2 = (3, 5.2)
antenna_3 = (6, 0)
antenna_4 = (9, -5.2)
antenna_5 = (9, 0)
antenna_6 = (9, 5.2)
antenna_7 = (9, 10.4)
antenna_8 = (12, 0)

maximum_distance = 8.7
antennas_coordinates = [antenna_1, antenna_2, antenna_3, antenna_4, antenna_5, antenna_6, antenna_7, antenna_8]

scaled_antennas = [(x*2, y*2) for x, y in antennas_coordinates]
scaled_maximum_distance = maximum_distance * 2

data = find_MIS(scaled_antennas, scaled_maximum_distance)