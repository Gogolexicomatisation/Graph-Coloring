from step3 import pulser_MIS

def pulser_color_graph(antennas_coordinates, distance):
    active_qubits = list(range(len(antennas_coordinates)))
    color_list = []
    while active_qubits != []:
        mis_bit_string = pulser_MIS(antennas_coordinates, distance, active_qubits)
        print("mis_string = ", mis_bit_string)
        color_list.append(mis_bit_string)
        active_qubits = [i for i, bit in enumerate(mis_bit_string) if bit == '0' and i in active_qubits]
        print("active_qubits = ", active_qubits)

    return color_list

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

color = pulser_color_graph(antennas, maximum_distance)
print(color)