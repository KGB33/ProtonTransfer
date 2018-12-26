from xyz import read_xyz, write_xyz
from Formulas import distance
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D graph
import matplotlib.pyplot as plt
import numpy as np


def main():
    file_name = 'h5o2_2cc_scan_sum'
    from_file_path = 'data/' + file_name + '.xyz'
    to_file_path = 'data/' + file_name + '_with_proton_indicator.xyz'
    all_steps = []

    # Read Files
    with open(from_file_path) as in_file:
        while True:
            try:
                all_steps.append(read_xyz(in_file))
            except ValueError:
                print('End of File')
                break

    # Plot Data
    num_atoms = len(all_steps[0].atom_types)
    proton_index = find_moving_hydrogen(all_steps[0], all_steps[-1])
    oxygen_indexes = [i for i in range(0, num_atoms) if all_steps[0].atom_types[i] == 'O']
    plot_data(all_steps, proton_index, oxygen_indexes)

    # Open out file
    with open(to_file_path, 'w') as out_f:
        # Format data for output
        for step, proton in zip(all_steps, track_proton(all_steps, proton_index, 1)):
            cords_out = []
            for atom in zip(step.coords):
                cords_out += atom
            cords_out += (proton, )
            cords_out = np.asarray(cords_out)
            atom_types_out = step.atom_types + ['p+', ]
            title_out = step.title
            # Write to file
            write_xyz(out_f, cords_out, title_out, atom_types_out)


def find_moving_hydrogen(step_one, step_last):
    max_change = 0
    moving_atom_index = None
    for i in range(0, len(step_one.coords)):
        if step_one.atom_types[i] != 'H':
            continue
        atom_one, atom_last = step_one.coords[i], step_last.coords[i]
        delta = distance(atom_one, atom_last)
        if delta > max_change:
            max_change = delta
            moving_atom_index = i
    return moving_atom_index


def plot_data(data, proton_index, oxygen_indexes, step=1):
    num_steps = len(data)

    # Oxygen Coords
    ox_coords = []
    for j in oxygen_indexes:
        temp = []
        for i in range(0, num_steps, step):
            temp += [data[i].coords[j], ]
        ox_coords += (temp, )
    y_os = [calculate_distance_from_atom(ox_coords[0], ox_coords[i]) for i in range(0, len(ox_coords))]

    # Hydrogen Coords
    hydrogen_coords = [data[i].coords[proton_index] for i in range(0, num_steps, step)]
    y_h = calculate_distance_from_atom(ox_coords[0], hydrogen_coords)

    # Proton Indicator Coords
    y_p = calculate_distance_from_atom(ox_coords[0], track_proton(data, proton_index, step))

    # Set up plot
    fig = plt.figure()
    ax = fig.gca()
    
    # Add Data
    xs = [x for x in range(0, num_steps, step)]
    for ox in y_os:
        ax.scatter(xs, ox)
    ax.scatter(xs, y_h, color='r', label='Hydrogen')
    print(len(xs), len(y_p))
    ax.scatter(xs, y_p, color='g', label='Proton Indicator')
    ax.legend()
    plt.show()


def calculate_distance_from_atom(atom_one, atom_two):
    result = []
    for i, j in zip(atom_one, atom_two):
        result += [distance(i, j)]
    return result


def track_proton(data, proton_index, delta):
    proton_position = []
    for i in range(0, len(data), delta):
        step = data[i]
        proton_indicator = None
        for atom, atom_name in zip(step.coords, step.atom_types):
            if atom_name == 'O':
                if distance(step.coords[proton_index], atom) < 1:
                    proton_indicator = atom
        if proton_indicator is None:
            proton_indicator = step.coords[proton_index]
        proton_position.append(proton_indicator)
    return proton_position
    
    
if __name__ == '__main__':
    main()
    quit()
