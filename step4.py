from step3 import pulser_MIS


def pulser_color_graph(antennas_coordinates, distance):
    active_qubits = list(range(len(antennas_coordinates)))
    color_list = []
    while active_qubits != []:
        mis_bit_string = pulser_MIS(antennas_coordinates, distance, active_qubits)
        #print("mis_string = ", mis_bit_string)
        color_list.append(mis_bit_string)
        active_qubits = [i for i, bit in enumerate(mis_bit_string) if bit == '0' and i in active_qubits]
        #print("active_qubits = ", active_qubits)

    return color_list