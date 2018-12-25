from abc import ABC, abstractmethod, abstractproperty
from Formulas import distance


class Atom(ABC):

    def __init__(self):
        """
        ABC For all atoms. x, y, z are the coords over time
        """
        self.x = []
        self.y = []
        self.z = []

    @abstractmethod
    def __str__(self):
        atom_name = 'Atom'
        if self.x and self.y and self.z:
            return 'This is {} atom at ({}, {}, {})'.format(atom_name, self.x[-1], self.y[-1], self.z[-1])
        return 'This is Atom atom at (Unknown Coords)'.format(atom_name)

    def current_pos(self):
        return [self.x[-1], self.y[-1], self.z[-1]]


class Hydrogen(Atom):

    def __init__(self, home=None):
        """
        Represents All Hydrogen atoms
        :param home (Optional): Oxygen atom that the Hydrogen is within one unit of. If no such atom exists, is None
        """
        super().__init__()
        self.home = home

    def find_home(self, ox_list):
        for ox in ox_list.atom_list:
            if distance(self.current_pos(), ox.current_pos()) < 1:
                self.home = ox
                return ox
        self.home = None
        return None

    def __str__(self):
        atom_name = 'Hydrogen'
        if self.x and self.y and self.z:
            return 'This is {} atom at ({}, {}, {})'.format(atom_name, self.x[-1], self.y[-1], self.z[-1])
        return 'This is {} atom at (Unknown Coords)'.format(atom_name)


class Oxygen(Atom):

    def __str__(self):
        atom_name = 'Oxygen'
        if self.x and self.y and self.z:
            return 'This is {} atom at ({}, {}, {})'.format(atom_name, self.x[-1], self.y[-1], self.z[-1])
        return 'This is {} atom at (Unknown Coords)'.format(atom_name)


class AtomList(ABC):

    # Will only accept atoms of type: (all)
    ATOM_TYPE = Atom

    def __init__(self, *args):
        """
        Initates the list with optional atoms, if an 'atom'
            is not the correct atom type, (or not even an atom)
            it is not added to the list

        :param args: (Optional) Atoms of type ATOM_TYPE
        """
        self.atom_list = []
        for element in args:
            if isinstance(element, self.ATOM_TYPE):
                self.atom_list.append(element)

    def add_atom(self, atom):
        """
        Adds an Atom to the Atom List
        :param atom: Atom to be added (Should be of the correct type)
        :return: None
        """
        if isinstance(atom, self.ATOM_TYPE):
            self.atom_list.append(atom)
        else:
            print(atom, " Was not added to :", self)


class HydrogenList(AtomList):

    ATOM_TYPE = Hydrogen

    def find_homes(self, ox_list):
        """
        Updates all the Hydrogen Atom's Homes
        :param ox_list: An OxygenList class
        :return: None
        """
        for hydrogen in self.atom_list:
            hydrogen.find_home(ox_list)


class OxygenList(AtomList):

    ATOM_TYPE = Oxygen


