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
    """
    Finds a hydrogen that is not bound to any oxygen or nitrogen atoms, if one exists

    :param data: Named tuple (oxygen, nitrogen, hydrogen, other_atoms)
        Data containing atom coordinate and sorted by atom type

    :return: vector
        coordinates of the un-bonded hydrogen
    """
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
    """
    Finds the donor atom based on number of hydrogen bonded to it

    :param data: Named tuple (oxygen, nitrogen, hydrogen, other_atoms)
        Data containing atom coordinate and sorted by atom type

    :return: vector
        coordinates of donor atom
    """

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

    :param step: namedtuple (atom_types, coords, title)
        the raw data from the .xyz file that was read in

    :return: namedtuple (oxygen, nitrogen, hydrogen, other_atoms)
        Data containing atom coordinate and sorted by atom type
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
    Formats data to pass into xyz.write_xyz

    :param data: namedtuple (atom_types, coords, title)
        Data to be added to
    :param out_file: file pointer
        File to be written to
    :param proton_coord: vector
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
    Plots the distance from the origin (0, 0, 0) of the proton indicator

    :param proton_coords: list of vectors
        Coords of the proton over time
    :param step: int (Default=1)
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
    """
    Work function that calcuates the coordinates of a proton indicator based off of the coordinates of all other atoms.

    :param data: Named tuple (oxygen, nitrogen, hydrogen, other_atoms)
        Data containing atom coordinate and sorted by atom type
    :param donor_coords: vector
        Coordinate of the donor atom

    :return: vector
        Coordinates of the proton indicator
    """
    possible_acceptors = find_possible_acceptors(data, donor_coords)

    # If there are no possible acceptors within given R_LIST, the proton indicator is at the donor
    if possible_acceptors is None:
        return donor_coords, donor_coords

    hydrogen_bonded_to_donor = find_hydrogen_bonded_to_donor(data, donor_coords)
    norm_factor = normalization_factor(possible_acceptors, hydrogen_bonded_to_donor, donor_coords)

    x_donor = donor_coords.copy()
    summation = 0
    for j in possible_acceptors:
        for m in hydrogen_bonded_to_donor:
            summation += weight_function(projected_donor_acceptor_ratio(j, m, donor_coords)) * j
    result = (x_donor + summation) / norm_factor
    return result, donor_coords


def find_hydrogen_bonded_to_donor(data, donor_coords):
    """
    Finds all hydrogen atoms currently bonded to the donor atom based off distance

    :param data: Named tuple (oxygen, nitrogen, hydrogen, other_atoms)
        Data containing atom coordinate and sorted by atom type
    :param donor_coords: vector
        Coordinate of the donor atom

    :return: list
        a list containing the coordinates of all hydrogen atoms bonded to the donor
    """
    hydrogen = []
    for hy in data.hydrogen:
        if np.dot(hy - donor_coords, hy - donor_coords) < CUT_OFF_DISTANCE_O_H:
            hydrogen.append(hy)
    return hydrogen


def find_possible_acceptors(data, donor_coords):
    """
    Finds possible Oxygen and Nitrogen atoms that could accept the proton based on distance from the donor coords

    :param data: Named tuple (oxygen, nitrogen, hydrogen, other_atoms)
        Data containing atom coordinate and sorted by atom type
    :param donor_coords: vector
        Coordinate of the donor atom

    :return: list
        a list containing the coordinate of possible acceptors
    """
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
    A stepped, 5th order polynomial dependant on x that determines the weight of x.
    X is the projected_donor_acceptor_ratio.

    :param x: float
        projected_donor_acceptor_ratio for some J, M

    :return: float
        When x ≥ 1:
            :returns: 0
        When 0 ≤ x < 1:
            :returns: A stepped, 5th order polynomial dependant on x
        When x < 0:
            :returns: 1
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

    :param js: iterator of vectors
        An iterator of possible acceptor vectors
    :param ms: iterator of vectors
        An iterator of hydrogen vectors
    :param donor_coords: vector
        coordinates of the donor atom

    :return: float
        Normalization factor
    """
    g = 1
    for j in js:
        for m in ms:
            g += weight_function(projected_donor_acceptor_ratio(j, m, donor_coords))
    return g


def projected_donor_acceptor_ratio(j, m, donor_coords):
    """
    Calculates a ratio indicating how close the hydrogen (m) is to the donor (donor coords) vs a possible acceptor (j).

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
    denominator = np.dot(abs(j - donor_coords), abs((j - donor_coords)))
    return numerator/denominator


if __name__ == '__main__':
    main()
    quit()
