from abc import ABC, abstractmethod
from Formulas import distance

CUT_OFF_DISTANCE = 1.005  # Cut off distance for H - O bonding, in 1 ≤ r ≤ 1.2, but the closer to 1 the better


class Atom(ABC):
    """
    Abstract Base Class for all atoms

    Attributes:
        x (numeric): x coordinate
        y (numeric): y coordinate
        z (numeric): z coordinate
    """

    def __init__(self, c=(None, None, None)):
        """
        :param c: (Optional array-like) Coordinates of current location in the form [x, y, z]
        """
        self.x, self.y, self.z = c

    @abstractmethod
    def __str__(self):
        pass

    def update_coords(self, c):
        """
        Updates Coords to [x, y, z]
        :param c: (Optional array-like) Coordinates of current location in the form [x, y, z]
        """
        self.x, self.y, self.z = c

    def current_pos(self):
        """
        :return: Current coordinates of self
        """
        return [self.x, self.y, self.z]


class Proton(Atom):
    """
    This class holds the positional data and the relationship
    between the proton and the other atoms in the data file.

    Attributes:
        :x (numeric): x coordinate
        :y (numeric): y coordinate
        :z (numeric): z coordinate
        :atom (Atom Object): The atom that the proton is attached to.
    """

    def __init__(self, c=(None, None, None)):
        """
        :param c: (Optional array-like) Coordinates of current location in the form [x, y, z]
        """
        self.atom = None
        super().__init__(c=c)

    def set_atom(self, atom):
        """
        :param atom: Atom Object
        """
        self.update_coords(atom.current_pos())
        self.atom = atom

    def __str__(self):
        """
        :return: Short description of the Proton Object
        """
        atom_name = 'Proton'
        if self.x is not None and self.y is not None and self.z is not None:
            return 'This {} is attached to: {}'.format(atom_name, self.x, self.y, self.z, self.atom)
        return 'This is {} at (Unknown Coords)'.format(atom_name)


class Hydrogen(Atom):
    """
    This class holds the positional data and the relationship
    between the Hydrogen atoms and the other atoms in the data file.

    Attributes:
        :x (numeric): x coordinate
        :y (numeric): y coordinate
        :z (numeric): z coordinate
        :home (Oxygen Object): Oxygen atom that the Hydrogen is within one unit of.
        :distance_to_home (numeric): distance from [x, y, z] to home
    """

    def __init__(self, c=(None, None, None), home=None):
        """
        :param c: (Optional array-like) Coordinates of current location in the form [x, y, z]
        :param home (Optional Oxygen Object): Oxygen atom that the Hydrogen is within one unit of.
                                                If no such atom exists, is None
        """
        super().__init__(c=c)
        self.home = home
        if home is not None and c is not None:
            self.distance_to_home = distance(home.current_pos(), c)
        else:
            self.distance_to_home = None

    def find_home(self, ox_list):
        """
        Finds the Oxygen Atom within CUT_OFF_DISTANCE from at list and sets it as home
        :global CUT_OFF_DISTANCE: Cut off distance for H - O bonding, in 1 ≤ r ≤ 1.2, but the closer to 1 the better
        :param ox_list: (OxygenList Object)
        :return: Home, If an home is found: returns Oxygen Object, else: returns None
        """
        global CUT_OFF_DISTANCE
        for ox in ox_list.atom_list:
            dist = distance(self.current_pos(), ox.current_pos())
            if dist < CUT_OFF_DISTANCE:
                self.home = ox
                self.distance_to_home = dist
                break
        else:  # if no-break
            self.home = None
            self.distance_to_home = 0
        return self.home

    def __str__(self):
        atom_name = 'Hydrogen'
        """
        :return: Short description of the Hydrogen Object
        """
        if self.x is not None and self.y is not None and self.z is not None:
            return 'This is {} atom at ({}, {}, {})'.format(atom_name, self.x, self.y, self.z)
        return 'This is {} atom at (Unknown Coords)'.format(atom_name)


class Oxygen(Atom):
    """
    This class holds the positional data and the relationship
    between the Oxygen atoms and the other atoms in the data file.

    Attributes:
        :x (numeric): x coordinate
        :y (numeric): y coordinate
        :z (numeric): z coordinate
    """

    def __init__(self, c=(None, None, None)):
        """
        :param c: (Optional array-like) Coordinates of current location in the form [x, y, z]
        """
        super().__init__(c=c)

    def __str__(self):
        """
        :return: Short description of the Oxygen Object
        """
        atom_name = 'Oxygen'
        if self.x is not None and self.y is not None and self.z is not None:
            return 'This is {} atom at ({}, {}, {})'.format(atom_name, self.x, self.y, self.z)
        return 'This is {} atom at (Unknown Coords)'.format(atom_name)


class AtomList(object):
    """
    Holds Atom Objects and provides methods to make sub-lists of a particular atom-type

    Attributes:
        :atom_list (list): List of ATOM_TYPE Objects
        :ATOM_TYPE (Atom Class): Only objects of this type can be added to atom_list
    """

    # Will only accept atoms of type: (all)
    ATOM_TYPE = Atom

    def __init__(self, *args):
        """
        Initiates the list with optional atoms, if an 'atom'
            is not the correct atom type, (or not even an atom)
            it is not added to the list

        :param args (Optional): Atoms of type ATOM_TYPE
        """
        self.atom_list = []
        for element in args:
            if isinstance(element, self.ATOM_TYPE):
                self.atom_list.append(element)

    def add_atom(self, atom):
        """
        Adds an Atom to the atom_list
        :param atom: (Object of type ATOM_TYPE) Atom to be added
        """
        if isinstance(atom, self.ATOM_TYPE):
            self.atom_list.append(atom)
        else:
            # print(atom, " Was not added to :", self)
            pass

    def make_hydrogen_list(self):
        """
        Creates a Hydrogen List containing all Hydrogen Atoms in atom_list
        :return: A Hydrogen list
        """
        hl = HydrogenList()
        for atom in self.atom_list:
                hl.add_atom(atom)
        return hl

    def make_oxygen_list(self):
        """
        Creates an Oxygen List containing all Oxygen Atoms in atom_list
        :return: An Oxygen List
        """
        oxl = OxygenList()
        for atom in self.atom_list:
            oxl.add_atom(atom)
        return oxl


class HydrogenList(AtomList):
    """
    Holds Hydrogen Objects and provides methods to manipulate the hydrogen atoms

    Attributes:
        :atom_list (list): List of ATOM_TYPE Objects
        :ATOM_TYPE (Hydrogen Class): Only objects of this type can be added to atom_list
    """

    # Will only accept atoms of type: (Hydrogen)
    ATOM_TYPE = Hydrogen

    def find_homes(self, ox_list):
        """
        Updates all the Hydrogen Atom's Homes
        :param ox_list: (OxygenList Object) Oxygen List object to find homes in
        """
        for hydrogen in self.atom_list:
            hydrogen.find_home(ox_list)


class OxygenList(AtomList):
    """
    Holds Oxygen Objects

    Attributes:
        :atom_list (list): List of ATOM_TYPE Objects
        :ATOM_TYPE (Oxygen Class): Only objects of this type can be added to atom_list
    """

    # Will only accept atoms of type: (Oxygen)
    ATOM_TYPE = Oxygen
