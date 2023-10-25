import pulser
import numpy as np
from pprint import pprint
from pulser import Pulse, Sequence, Register
from pulser.devices import Chadoq2
from pulser.waveforms import RampWaveform, BlackmanWaveform
from pulser_simulation import QutipEmulator
import networkx as nx


def mis_hamiltonian(graph):
    # This is a simplified version. In a real-world scenario, you'd need to consider
    # the specific interactions and energy levels of the Rydberg atoms.
    H = np.zeros((2**len(graph.nodes), 2**len(graph.nodes)))
    for edge in graph.edges:
        i, j = edge
        # Penalize if both i and j are in the excited state
        H[2**i + 2**j, 2**i + 2**j] += 1
    return H

def rescale_layout(layout, scale_factor):
    """Rescale the coordinates of a layout."""
    return {node: (x*scale_factor, y*scale_factor) for node, (x, y) in layout.items()}


G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4)])
layout = nx.spring_layout(G)
scaled_layout = rescale_layout(layout, 10)

# Create a register from the rescaled layout
reg = Register({f'q{i}': scaled_layout[i] for i in G.nodes()})

# Create a sequence
seq = Sequence(reg, Chadoq2)

rydberg_radius = 5 # TO MODIFY
seq.declare_channel('ryd', 'rydberg_global', initial_target=rydberg_radius)

# Define a π-pulse
duration = 1000  # Typical: ~1 µsec
pi_pulse = Pulse.ConstantDetuning(BlackmanWaveform(duration, np.pi), 0.0, 0.0)

# Add the π-pulse to the sequence
seq.add(pi_pulse, 'ryd')

sim = QutipEmulator.from_sequence(seq)
results = sim.run()

final_state = results.states[-1]
probabilities = np.abs(final_state.data.toarray())**2

# Extract the most probable state
most_probable_state = np.argmax(probabilities)
binary_representation = format(most_probable_state, f'0{len(G.nodes)}b')

# Nodes in the MIS are those corresponding to bits set to 1
mis = [i for i, bit in enumerate(binary_representation) if bit == '1']
print("Maximum Independent Set:", mis)