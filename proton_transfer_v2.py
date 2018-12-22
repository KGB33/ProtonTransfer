from xyz import read_xyz, write_xyz
from Formulas import distance
from Exceptions import AtomDistanceError
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D graph
import matplotlib.pyplot as plt
import numpy as np


def main():
    # file_name = 'h5o2_2cc_scan_sum' # Two Water Molecules
    file_name = 'h13o6_2_scan_sum'  # Six Water molecules
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
    oxygen_indexes = [find_closest_oxygen(all_steps[0], proton_index), find_closest_oxygen(all_steps[-1], proton_index)]
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
    """
    Finds the closest Oxygen to each Hydrogen, then finds the hydrogen that moves farthest from the Ox
    :param step_one: 1st data Step
    :param step_last: Last Data Step
    :return: Index of the Free Hydrogen
    """

    # Part 0, get the indexes of each hydrogen
    hydrogen = {}  # {h_index: index_of_closes_oxygen}
    for i in range(0, len(step_one.atom_types)):
        if step_one.atom_types[i] == 'H':
            hydrogen.update({i: None})

    # Part One, Find the Oxygen closest to each Hydrogen
    for index in hydrogen:
        hydrogen[index] = find_closest_oxygen(step_one, index)

    # Part Two, Figure out which one moved the most
    max_distance = 0
    for h_index in hydrogen:
        dist = distance(step_last.coords[h_index], step_last.coords[hydrogen[h_index]])
        if dist > max_distance:
            max_distance = dist
            index = h_index
    return index


def find_closest_oxygen(step, hydrogen_index):
    """
    :param step: the current data step
    :param hydrogen_index: The index of the hydrogen to find the closet Oxygen to
    :return: The index of the closest Oxygen to the hydrogen provided
    """
    min_distance = 1000000  # Really big
    index = 0
    for i in range(0, len(step.atom_types)):
        if step.atom_types[i] == 'O':
            cur_dist = distance(step.coords[hydrogen_index], step.coords[i])
            if cur_dist < min_distance:
                min_distance = cur_dist
                index = i
    if min_distance >= 1000000:  # Checks to make sure min_distance was updated
        raise AtomDistanceError
    return index


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
    n = 0
    for ox in y_os:
        label = 'Oxygen ' + str(n)
        ax.scatter(xs, ox, label=label)
        n += 1
    ax.scatter(xs, y_h, color='r', label='Hydrogen')
    print(len(xs), len(y_p))
    ax.scatter(xs, y_p, color='y', label='Proton Indicator')
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
