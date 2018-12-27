"""
From https://github.com/pele-python/pele/blob/master/pele/utils/xyz.py
Thanks js850 !


Updated to python 3.7
"""

"""
tools for reading from and writing to .xyz files

.. autosummary::
    :toctree: generated/

    read_xyz
    write_xyz
"""

import numpy as np
from itertools import cycle
from collections import namedtuple

__all__ = ["read_xyz", "write_xyz"]


def read_xyz(fin):
    """ read a xyz file from file handle

    Parameters
    ----------
    fin : file handle
        file to read from

    Returns
    -------
    fin : open file
    xyz : namedtuple
        returns a named tuple with coords, title and list of atom_types.

    See Also
    --------
    write_xyz

    """
    try:
        num_atoms = int(fin.readline())
        title = fin.readline()[:-1]
        coords = np.zeros([num_atoms, 3], dtype="float64")
        atom_types = []
        for x in coords:
            line = fin.readline().split()
            atom_types.append(line[0])
            x[:] = [float(x) for x in line[1:4]]

        return namedtuple("XYZFile", ["coords", "title", "atom_types"])\
            (coords, title, atom_types)
    except ValueError:
        # End of file reached
        return None


def write_xyz(file_out, coords, title="", atom_types=("A",)):
    """ write a xyz file from file handle

    Writes coordinates in xyz format. It uses atom_types as names. The list is
    cycled if it contains less entries than there are coordinates,

    One can also directly write xyz data which was generated with read_xyz.

    # >>> xx = read_xyz("in.xyz")
    # >>> write_xyz(open("out.xyz", "w"), *xx)

    Parameters
    ----------
    file_out : an open file
    coords : np.array
        array of coordinates
    title : title section, optional
        title for xyz file
    atom_types : iterable
        list of atom_types.

    See Also
    --------
    read_xyz

    """
    file_out.write(" %d\n%s\n" % (coords.size / 3, title))
    for x, atom_type in zip(coords.reshape(-1, 3), cycle(atom_types)):
        file_out.write("\t\t{} {:14.06f} {:14.06f} {:14.06f}\n".format(atom_type, x[0], x[1], x[2]))
