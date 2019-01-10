from xyz import read_xyz, write_xyz
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple
from argparse import ArgumentParser

# Constants!
CUT_OFF_DISTANCE_O_H = 1.005  # must be in 1 ≤ r ≤ 1.2, but the closer to 1 the better
CUT_OFF_DISTANCE_N_H = 1.200  # must be in 1.2 ≤ r ≤ 1.4 but the closer to 1.2 the better
R_LIST = 2.60                 # From paper, see readme for citations
"""
Cut off distance for H - O bonding and H - N bonding respectively 
experimental found by looking at the graph (-g command line arg) with minimal to no outliers
"""


# Arg Parser
def get_args(args=None):
    """
    Default Function to parse command line arguments
    """
    parser = ArgumentParser(description='See header of script')
    parser.add_argument(
        '-i',
        '--infile_name',
        help='Input File Name',
        required=True)
    parser.add_argument(
        '-g',
        '--graph',
        help='Graphs The dist of proton indicator from (0,0,0)',
        required=False)
    return parser.parse_args(args)


def main():
    """
     - Reads In a .xyz file
     - Creates an Atom object for each atom in Step
     - Calculates which atom is acting as the proton transfer
     - adds a proton indicator and writes each step to an out_file
    """

    args = get_args(None)  # Gets args from command line

    """ File Name(s) """
    file_name = args.infile_name
    # In File Path
    from_file_path = file_name + '.xyz'
    # Out File Path
    to_file_path = file_name + '_with_proton_indicator.xyz'

    # Instance Variables
    proton_coords = []  # only used for graphing

    # Read Files
    data_generator = read_xyz(from_file_path)
    with open(to_file_path, 'w') as out_file:
        # Calculate Proton Indicator position for all steps
        # and change Donor if necessary
        for step in data_generator:
                data = sort_atoms(step)
                donor_coord = find_donor(data)

                if donor_coord is None:
                    proton_coord = find_lone_hydrogen(data)
                else:
                    # find Proton Indicator
                    proton_coord, donor_coord = find_proton_indicator(data, donor_coord)

                if args.graph:
                    proton_coords += [proton_coord, ]

                # Write Data
                write_data(step, out_file, proton_coord)

        # Plot Data
        if args.graph:
            plot_data(proton_coords)


def find_lone_hydrogen(data):
    for h in data.hydrogen:
        for ox in data.oxygen:
            if np.dot(h - ox, h - ox) <= CUT_OFF_DISTANCE_O_H:
                break
        else:
            return h
    for h in data.hydrogen:
        for n in data.nitrogen:
            if np.dot(h - n, h - n) <= CUT_OFF_DISTANCE_N_H:
                break
        else:
            return h


def find_donor(data):

    # test Oxygen first

    for ox in data.oxygen:
        num_hy = len([1 for h in data.hydrogen if np.dot(ox - h, ox - h) < CUT_OFF_DISTANCE_O_H])
        if num_hy == 3:
            return ox

    # Test Nitrogen
    for n in data.nitrogen:
        num_hy = len([1 for h in data.hydrogen if np.dot(n - h, n - h) < CUT_OFF_DISTANCE_N_H])
        if num_hy == 4:
            return n
    # No atoms had a spare hydrogen to donate
    return None


def sort_atoms(step):
    """
    sort atoms into atom_types
    :param step: namedtuple
        fields:
            atom_types: atom names
            coords: atom coords
            title: step title (not used)
    :return: namedtuple
        fields:
            hydrogen
            oxygen
            nitrogen
            other_atoms
    """
    hydrogen = []
    oxygen = []
    nitrogen = []
    other_atoms = []
    for atom, coords in zip(step.atom_types, step.coords):
        if atom == 'O':
            oxygen.append(coords)
        elif atom == 'N':
            nitrogen.append(coords)
        elif atom == 'H':
            hydrogen.append(coords)
        else:
            other_atoms.append(coords)
            
    return namedtuple('SortedAtomCoords', ['hydrogen', 'oxygen', 'nitrogen', 'other_atoms']
                      )(hydrogen, oxygen, nitrogen, other_atoms)


def write_data(data, out_file, proton_coord):
    """
    Formats data to pass into write_xyz

    :param data: (namedtuple)
        Data to be added to
    :param out_file: (File Pointer)
        File to be written to
    :param proton_coord: (1x3 Array-Like)
        Coordinate of proton indicator to add
    """
    # Format out_coords
    out_coords = []
    for i in zip(data.coords):
        out_coords += i
    out_coords += (proton_coord,)
    out_coords = np.asarray(out_coords)
    # print(out_coords)

    # Format out_atom_types
    out_atom_types = data.atom_types + ['DUM']

    # Format out_title
    out_title = data.title

    # Write to file
    write_xyz(out_file, out_coords, out_title, out_atom_types)


def plot_data(proton_coords, step=1):
    """
    Plots the length (aka distance from the origin (0, 0, 0)) of the proton indicator

    :param proton_coords: ( Nx3, Array-like)
        Coords of the proton over time
    :param step: (int) (Default=1)
        Number of steps between points, lower numbers will have more accuracy, Minimum step is one
    """
    # Set up plot
    fig = plt.figure()
    ax = fig.gca()

    # Add Data
    xs = [x for x in range(0, len(proton_coords), step)]
    y_p = [np.dot(np.asarray([0, 0, 0]) - proton_coords[x], np.asarray([0, 0, 0]) - proton_coords[x])
           for x in range(0, len(proton_coords), step)]
    ax.scatter(xs, y_p, color='y', label='Proton Indicator')

    # Show plot
    ax.legend()
    plt.show()


def find_proton_indicator(data, donor_coords):
    possible_acceptors = find_possible_acceptors(data, donor_coords)
    #  print(f'Possible accept: {possible_acceptors}')
    #  print(f'Donor Coords {donor_coords}')

    # If there are no possible acceptors within given R_LIST, the proton indicator is at the donor
    if possible_acceptors is None:
        return donor_coords, donor_coords

    hydrogen_bonded_to_donor = find_hydrogen_bonded_to_donor(data, donor_coords)
    #  print(f'Hydo bonded: {hydrogen_bonded_to_donor}')
    norm_factor = normalization_factor(possible_acceptors, hydrogen_bonded_to_donor, donor_coords)
    #  print(f'Norm Factor {norm_factor}')

    x_donor = donor_coords.copy()
    summation = 0
    for j in possible_acceptors:
        for m in hydrogen_bonded_to_donor:
            summation += weight_function(projected_donor_acceptor_ratio(j, m, donor_coords)) * j
    result = (x_donor + summation) / norm_factor
    #  print('r', result)
    #  input()
    return result, donor_coords


def find_hydrogen_bonded_to_donor(data, donor_coords):
    hydrogen = []
    for hy in data.hydrogen:
        if np.dot(hy - donor_coords, hy - donor_coords) < CUT_OFF_DISTANCE_O_H:
            hydrogen.append(hy)
    return hydrogen


def find_possible_acceptors(data, donor_coords):
    poss_acceptors = []
    for ox in data.oxygen:
        dist = np.dot(ox - donor_coords, ox - donor_coords)
        if dist <= R_LIST and dist != 0:
            poss_acceptors.append(ox)

    for n in data.nitrogen:
        dist = np.dot(n - donor_coords, n - donor_coords)
        if dist < R_LIST and dist != 0:
            poss_acceptors.append(n)

    return poss_acceptors


def weight_function(x):
    """
    g(x)
    Determines the weight of x depending on its value
    :param x: (float)
    :return: (float)
    """
    if x >= 1:
        return 0
    elif x < 0:
        return 1
    else:  # 0 <= x < 1
        return -6 * pow(x, 5) + 15 * pow(x, 4) - 10 * pow(x, 3) + 1


def normalization_factor(js, ms, donor_coords):
    """
    The normalization factor
    :return: (float)
    """
    g = 1
    for j in js:
        for m in ms:
            g += weight_function(projected_donor_acceptor_ratio(j, m, donor_coords))
    return g


def projected_donor_acceptor_ratio(j, m, donor_coords):
    """
    AKA Pjm from paper
    :param j: vector
        possible acceptor vector
    :param m: vector
        hydrogen vector
    :param donor_coords: vector
        Coords of donor atom
    :return: float
        Donor-Acceptor ratio
    """
    numerator = np.dot((m - donor_coords), (j - donor_coords))
    denominator = np.dot(j - donor_coords, j - donor_coords) ** 2
    return numerator/denominator


if __name__ == '__main__':
    main()
    quit()
