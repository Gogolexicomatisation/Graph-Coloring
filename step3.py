import pulser
import numpy as np
from pprint import pprint
from pulser import Pulse, Sequence, Register
from pulser.devices import Chadoq2
from pulser.waveforms import RampWaveform, BlackmanWaveform
from pulser_simulation import QutipEmulator
from graph import Graph
from step1 import model_antenna_frequency


def mis_hamiltonian(graph):
    # This is a simplified version. In a real-world scenario, you'd need to consider
    # the specific interactions and energy levels of the Rydberg atoms.
    H = np.zeros((2**len(graph.nodes), 2**len(graph.nodes)))
    for edge in graph.edges:
        i, j = edge
        # Penalize if both i and j are in the excited state
        H[2**i + 2**j, 2**i + 2**j] += 1
    return H

def pulser_MIS(antennas_coordinates, distance, active_qubits=None):
    if active_qubits is None:
        active_qubits = list(range(len(antennas_coordinates)))
    active_coords = [antennas_coordinates[i] for i in active_qubits]
    reg = Register.from_coordinates(active_coords)
    #reg.draw(blockade_radius=distance, draw_half_radius=True, draw_graph=True)

    seq = Sequence(reg, Chadoq2)

    rydberg_radius = distance
    seq.declare_channel('ryd', 'rydberg_global', initial_target=rydberg_radius)

    # Define a π-pulse
    duration = 1000  # Typical: ~1 µsec
    # pi_pulse = Pulse.ConstantDetuning(BlackmanWaveform(duration, 2*np.pi), 0.0, 0.0)
    pi_pulse = Pulse.ConstantPulse(duration, 2*np.pi, 0.0, 0.0)

    # Add the π-pulse to the sequence
    seq.add(pi_pulse, 'ryd')

    sim = QutipEmulator.from_sequence(seq)
    results = sim.run()

    final_state = results.states[-1]
    probabilities = np.abs(final_state.data.toarray())**2

    #print(probabilities)
    # Extract the most probable state
    most_probable_state = np.argmax(probabilities)
    binary_representation = format(most_probable_state, f'0{len(active_coords)}b')

    # Nodes in the MIS are those corresponding to bits set to 1
    mis = []
    full_bitstring = ['0'] * len(antennas_coordinates)
    for i, bit in enumerate(binary_representation):
        full_bitstring[active_qubits[i]] = bit

    for i in range(len(full_bitstring)):
        if full_bitstring[i] == '1':
            mis.append(i+1)
    print("Maximum Independent Set:", mis)

    return ''.join(full_bitstring)


antenna_1 = (0, 0)
antenna_2 = (0, 7)
antenna_3 = (0, 14)
# antenna_4 = (9, -5.2)
# antenna_5 = (9, 0)
# antenna_6 = (9, 5.2)
# antenna_7 = (9, 10.4)
# antenna_8 = (12, 0)

antennas = [antenna_1, antenna_2, antenna_3]
maximum_distance = 10
# scale_factor = 2
# scaled_antennas = [(x*scale_factor, y*scale_factor) for x, y in antennas]
# scaled_maximum_distance = maximum_distance * scale_factor

# adjacent_list = model_antenna_frequency(antennas)[0]

# graph = Graph(len(antennas))
# graph.add_adjacency_list(adjacent_list)
# graph.visualize()

active_qubits = list(range(len(antennas)))
phase1 = pulser_MIS(antennas, maximum_distance)
#print(phase1)


active_qubits = [i for i, bit in enumerate(phase1) if bit == '0' and i in active_qubits]
#print(active_qubits)
phase2 = pulser_MIS(antennas, maximum_distance, active_qubits)
#print(phase2)
active_qubits = [i for i, bit in enumerate(phase2) if bit == '0' and i in active_qubits]
#print(active_qubits)
