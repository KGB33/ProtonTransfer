"""
Reads in an xyz file.
finds the Free Hydrogen, then adds a proton indcator
to indicate where the Charge of the Hyrdorgen is located.
"""
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D graph
from xyz import read_xyz, write_xyz
import matplotlib.pyplot as plt
import numpy as np

H_INDEX = 1
O_ONE_INDEX = 0
O_TWO_INDEX = 4

def main():

    # Variables
    globals()
    step = 0
    proton_position, O_one_position, O_two_position, H_position = [], [], [], []
    file_name = 'h5o2_2cc_scan_sum'
    from_file_path = 'data/' + file_name + '.xyz'
    to_file_path = 'data/' + file_name + '_with_proton_indicator.xyz'

    # Open from file
    with open(from_file_path) as in_f, open(to_file_path, 'w') as out_f:
        while in_f:
            try:
                data = read_xyz(in_f)
                step += 1
            except ValueError:
                break

            # print the data!
            # compare_atom_distance(data, index=H_INDEX)

            # Do stuff with the data!
            new_atom = None
            for atom, atom_name in zip(data.coords, data.atom_types):
                if atom_name == 'O':
                    if distance(data.coords[H_INDEX], atom) < 1:
                        new_atom = atom
            if new_atom is None:
                new_atom = data.coords[H_INDEX]
            proton_position.append(new_atom)
            O_one_position.append(data.coords[O_ONE_INDEX])
            O_two_position.append(data.coords[O_TWO_INDEX])
            H_position.append(data.coords[H_INDEX])

            # Format data for output
            cords_out = []
            for atom in zip(data.coords):
                cords_out += atom
            cords_out += (new_atom, )
            cords_out = np.asarray(cords_out)
            atom_types_out = data.atom_types + ['p+', ]
            title_out = data.title

            # Write to file
            write_xyz(out_f, cords_out, title_out, atom_types_out)
    # plot position of proton over time
    #plot_position(proton_position, O_one_position, O_two_position, H_position)
    plot_distance_from_o_one(proton_position, O_one_position, O_two_position, H_position)


def compare_atom_distance(data, index=1):
    print("\n\n\n{}".format(data.title))
    for atom, atom_name in zip(data.coords, data.atom_types):
        print("The distance between the 1st H and the {} atom is:"
              "\n\t{} units".format(atom_name, distance(data.coords[index], atom)))


def plot_position(proton, o_one, o_two, h):
    xs, ys, zs = [], [], []
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for c in proton:
        xs += [c[0], ]
        ys += [c[1], ]
        zs += [c[2], ]
    ax.scatter(xs, ys, zs, color='g', label='Proton Indicator')
    for c in o_one:
        xs += [c[0], ]
        ys += [c[1], ]
        zs += [c[2], ]
    ax.scatter(xs, ys, zs, color='c', label='1st Oxygen')
    for c in o_two:
        xs += [c[0], ]
        ys += [c[1], ]
        zs += [c[2], ]
    ax.scatter(xs, ys, zs, color='b', label='2nd Oxygen')
    for c in h:
        xs += [c[0], ]
        ys += [c[1], ]
        zs += [c[2], ]
    ax.scatter(xs, ys, zs, color='r', label='Hydrogen')
    ax.legend()
    plt.show()


def plot_distance_from_o_one(proton, o_one, o_two, h):
    xs = [x for x in range(0, len(proton))]
    ys_p, ys_o, ys_h = [], [], []
    fig = plt.figure()
    ax = fig.gca()
    for i, j, k, m in zip(o_one, proton, o_two, h):
        ys_p += [distance(i, j), ]
        ys_o += [distance(i, k), ]
        ys_h += [distance(i, m), ]
    print("XS: {}"
          "\nYS_P: {}"
          "\nYS_O: {}"
          "\nYS_H: {}".format(len(xs), len(ys_p), len(ys_o), len(ys_h)))
    ax.scatter(xs, [0 for _ in range(0, len(xs))], color='c', label='1st Oxygen')
    ax.scatter(xs, ys_o, color='b', label='2nd Oxygen')
    ax.scatter(xs, ys_h, color='r', label='Hydrogen')
    ax.scatter(xs, ys_p, color='g', label='Proton Indicator')
    ax.legend()
    plt.show()


def distance(cord_1, cord_2):
    sum_squares = 0
    for i, j in zip(cord_1, cord_2):
        sum_squares += pow(i - j, 2)
    return np.sqrt(sum_squares)


main()
quit()
