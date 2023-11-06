import pulser
import numpy as np
from pprint import pprint
from pulser import Pulse, Sequence, Register
from pulser.devices import MockDevice
from pulser.waveforms import RampWaveform, BlackmanWaveform, ConstantWaveform
from pulser_simulation import QutipBackend


def pulser_MIS(antennas_coordinates, distance, active_qubits=None):
    if active_qubits is None:
        active_qubits = list(range(len(antennas_coordinates)))
    active_coords = [antennas_coordinates[i] for i in active_qubits]
    reg = Register.from_coordinates(active_coords)
    #reg.draw(blockade_radius=distance, draw_half_radius=True, draw_graph=True)

    omega =  MockDevice.rabi_from_blockade(distance)

    seq = Sequence(reg, MockDevice)
    seq.declare_channel('ch', 'rydberg_global')

    omega_wf_1 = RampWaveform(3000, 0, omega)   
    delta_wf_1 = ConstantWaveform(3000, -20)
    pulse1 = Pulse(omega_wf_1, delta_wf_1, 0)
    seq.add(pulse1, 'ch')


    omega_wf_2 = ConstantWaveform(10000, omega)  
    delta_wf_2 = RampWaveform(10000, -20, 20) 
    pulse2 = Pulse(omega_wf_2, delta_wf_2, 0)
    seq.add(pulse2, 'ch')


    omega_wf_3 = RampWaveform(3000, omega, 0)   
    delta_wf_3 = ConstantWaveform(3000, 20)
    pulse3 = Pulse(omega_wf_3, delta_wf_3, 0)
    seq.add(pulse3, 'ch')

    sim= QutipBackend(seq)
    results=sim.run()
    
    # Extract the most probable state
    most_probable_state = str(max(results.sample_final_state(1000)))
    binary_representation = most_probable_state.zfill(len(active_coords))

    # Nodes in the MIS are those corresponding to bits set to 1
    mis = []
    full_bitstring = ['0'] * len(antennas_coordinates)
    for i, bit in enumerate(binary_representation):
        full_bitstring[active_qubits[i]] = bit

    for i in range(len(full_bitstring)):
        if full_bitstring[i] == '1':
            mis.append(i+1)
    print("Maximum Independent Set23434234:", mis)

    return ''.join(full_bitstring)
