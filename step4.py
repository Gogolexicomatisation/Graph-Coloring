from step3 import pulser_MIS

# Graph coloring
def pulser_color_graph(antennas_coordinates, distance):
    # List storing the numbers associated with the qubits that are still in use.
    active_qubits = list(range(len(antennas_coordinates)))
    # List storing bitstring, each bitstring is associated with a different color
    color_list = []
    while active_qubits != []:
        mis_bit_string = pulser_MIS(antennas_coordinates, distance, active_qubits)
        color_list.append(mis_bit_string)
        active_qubits = [i for i, bit in enumerate(mis_bit_string) if bit == '0' and i in active_qubits]

    return color_list