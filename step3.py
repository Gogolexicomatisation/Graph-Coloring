from pulser import Pulse, Sequence, Register
from pulser.devices import MockDevice
from pulser.waveforms import InterpolatedWaveform
from pulser_simulation import QutipBackend

# MIS without constraint
def pulser_MIS(antennas_coordinates, distance, active_qubits=None):
    if active_qubits is None:
        active_qubits = list(range(len(antennas_coordinates)))
    # Place the qubits corresponding to the remaining uncolored edges
    active_coords = [antennas_coordinates[i] for i in active_qubits]
    reg = Register.from_coordinates(active_coords)

    omega =  MockDevice.rabi_from_blockade(distance)

    seq = Sequence(reg, MockDevice)
    
    # Add pulse 
    seq.declare_channel('ch', 'rydberg_global')

    omega_wf = InterpolatedWaveform(10000, [0, omega, 0])
    delta_wf = InterpolatedWaveform(10000, [-20, 0, 20])
    pulse = Pulse(omega_wf, delta_wf, 0)
    seq.add(pulse, 'ch')

    # Run simulation
    sim= QutipBackend(seq)
    results=sim.run()
    
    # Extract the most probable state
    state_counts = results.sample_final_state(1000)
    most_probable_state = max(state_counts, key=state_counts.get)
    most_probable_state_str = str(most_probable_state)
    binary_representation = most_probable_state_str.zfill(len(active_coords))
    
    print("\033[33m" + str(state_counts) + "\033[0m")

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
