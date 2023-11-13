import pulser
import numpy as np
from pulser import Pulse, Sequence, Register
from pulser_simulation import QutipBackend
from pulser.devices import MockDevice
from pulser.waveforms import InterpolatedWaveform
from pulser.register.register_layout import RegisterLayout
from pulser.register.special_layouts import (SquareLatticeLayout, TriangularLatticeLayout,)
import random
from pprint import pprint

# Create a list of traps coordinates (input of RegisterLayout)
def generate_unique_traps(num_traps, antenna_coords):
    nb_traps = num_traps - len(antenna_coords)
    while True:
        traps = np.random.randint(0, 30, size=(nb_traps, 2))
        traps = traps - np.mean(traps, axis=0)

        # Check for unique trap coordinates
        unique_traps = np.unique(traps, axis=0)
        if len(unique_traps) != nb_traps:
            continue
        
        # Check if any trap coordinates overlap with antenna coordinates
        overlap = any(np.any(np.all(traps == antenna_coord, axis=1)) for antenna_coord in antenna_coords)

        if not overlap:
            return traps
        
# Create a dictionary associating the qubits with their corresponding trap's position   
def create_qubit_dictionary(layout, num_qubits, coordinates):
    qubit_dictionary = {}
    for i in range(num_qubits):
        qubit_name = f'q{i}'
        trap_ = layout.get_traps_from_coordinates(coordinates[i])[0]
        qubit_dictionary[qubit_name] = trap_
    return qubit_dictionary


def realistic_pulser_MIS(antennas_coordinates, distance, active_qubits=None):
    if active_qubits is None:
        active_qubits = list(range(len(antennas_coordinates)))
    # Place the qubits corresponding to the remaining uncolored edges
    active_coords = [antennas_coordinates[i] for i in active_qubits]
    
    nb_qubits = len(active_coords)
    num_traps = nb_qubits * 3
    traps = generate_unique_traps(num_traps, active_coords)
    traps = np.concatenate([active_coords, traps])

    # Creating the layout
    layout = RegisterLayout(traps)
    
    map_register = layout.make_mappable_register(n_qubits=nb_qubits)

    sequence = Sequence(map_register, MockDevice)
    
    # Add pulse 
    sequence.declare_channel('ch', 'rydberg_global')

    omega =  MockDevice.rabi_from_blockade(distance)

    omega_wf = InterpolatedWaveform(10000, [0, omega, 0])
    detuning_wf = InterpolatedWaveform(10000, [-20, 0, 20])
    pulse = Pulse(omega_wf, detuning_wf, 0)

    sequence.add(pulse, 'ch')
    
    # Build Sequence
    qubit_dictionnary = create_qubit_dictionary(layout=layout, num_qubits=nb_qubits, coordinates=active_coords)
    build_sequence = sequence.build(qubits=qubit_dictionnary)
    
    # Run simulation
    sim = QutipBackend(build_sequence)
    results = sim.run()
    
    print(results.sample_final_state(1000))
    
    # Extract the most probable state
    state_counts = results.sample_final_state(1000)
    most_probable_state = max(state_counts, key=state_counts.get)
    most_probable_state_str = str(most_probable_state)
    binary_representation = most_probable_state_str.zfill(len(active_coords))

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
