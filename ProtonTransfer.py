from xyz import read_xyz, write_xyz
from Formulas import distance
from Exceptions import UnknownAtomError
import matplotlib.pyplot as plt
import numpy as np
from Atoms import Hydrogen, Oxygen, Proton, AtomList
from functools import partial
from collections import namedtuple


def main():
    """
     - Reads In a .xyz file
     - Creates an Atom object for each atom in Step
     - Calculates which atom is acting as the proton transfer
     - adds a proton indicator and writes each step to an out_file
    """

    # TODO: switch over to using path module
    """ File Name(s) """
    file_name = 'h5o2_2cc_scan_sum'  # Two Water Molecules
    # file_name = 'h13o6_2_scan_sum'  # Six Water molecules

    # In File Path
    from_file_path = 'data/' + file_name + '.xyz'

    # Out File Path
    to_file_path = 'data/' + file_name + '_with_proton_indicator.xyz'

    # Instance Variables
    proton_coords = []

    # Read Files
    with open(from_file_path) as in_file, open(to_file_path, 'w') as out_file:
        for data in iter(partial(read_xyz, in_file), None):

                # Create Atom Objects for each atom
                atom_list = atom_factory(data)
                h_list = atom_list.make_hydrogen_list()
                ox_list = atom_list.make_oxygen_list()
                n_list = atom_list.make_nitrogen_list()

                # Find the proton and add it's Coords
                proton_coords += [find_proton(h_list, ox_list, n_list)]

                # Write Data
                write_data(data, out_file, proton_coords)

        # Plot Data
        plot_data(proton_coords)


def write_data(data, out_file, proton_coords):
    """
    Formats data to pass into write_xyz

    :param data: (namedtuple)
        Data to be added to
    :param out_file: (File Pointer)
        File to be written to
    :param proton_coords: (Nx3 Array-Like)
        Coordinate of proton indicator to add
    """
    # Format out_coords
    out_coords = []
    for i in zip(data.coords):
        out_coords += i
    out_coords += (proton_coords[-1],)
    out_coords = np.asarray(out_coords)

    # Format out_atom_types
    out_atom_types = data.atom_types + ['p+']

    # Format out_title
    out_title = data.title

    # Write to file
    write_xyz(out_file, out_coords, out_title, out_atom_types)


def find_proton(h_list, ox_list, n_list):
    """
    Finds the Coordinates of the proton by finding
        the Oxygen with 3 residents,
        the Nitrogen with 4 residents,
        or the Hydrogen without a home

    :param h_list: (HydrogenList)

    :param ox_list: (OxygenList)

    :param n_list: (NitrogenList)

    :return: (1x3 Array-Like)
        Coordinates of proton, [x, y, z]
    """
    # Variables
    proton_indicator = Proton()
    homeless = []

    # Calculate Homes for each Hydrogen Atom
    h_list.find_homes(ox_list, n_list)

    # Find any Hydrogen atoms without a Home
    for h in h_list.atom_list:
        if h.home is None:
            homeless.append(h)

    # Finds the Homeless Hydrogen atom farthest from an Oxygen
    if homeless:
        max_h = homeless[0]
        for h in homeless:
            if h.distance_to_closest_ox > max_h.distance_to_closest_ox:
                max_h = h
        proton_indicator.set_atom(homeless[0])

    # If no Hydrogen is homeless, it finds the oxygen with 3 residents
    else:
        for ox in ox_list.atom_list:
            residents = 0
            for h in h_list.atom_list:
                if h.home == ox:
                    residents += 1
            if residents >= 3:
                proton_indicator.set_atom(ox)

    return proton_indicator.current_pos()


def atom_factory(data: namedtuple) -> AtomList:
    """
    Takes in namedtuple Data and creates atoms and adds them to an AtomList

    :param data: (namedtuple)
        Named Tuple with fields coords, atom_types, title

    :return: (AtomList)
        AtomList with atoms created from data
    """
    atom_list = AtomList()
    for atom, coords in zip(data.atom_types, data.coords):
        if atom == 'H':
            atom_list.add_atom(Hydrogen(c=coords))
        elif atom == 'O':
            atom_list.add_atom(Oxygen(c=coords))
        else:
            raise UnknownAtomError
    return atom_list


def plot_data(proton_coords, step=1):
    """
    Plots distance of the proton indicator from the origin (0, 0, 0)

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
    y_p = [distance([0, 0, 0], proton_coords[x]) for x in range(0, len(proton_coords), step)]
    ax.scatter(xs, y_p, color='y', label='Proton Indicator')

    # Show plot
    ax.legend()
    plt.show()


if __name__ == '__main__':
    main()
    quit()
