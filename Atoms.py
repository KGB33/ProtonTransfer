from abc import ABC, abstractmethod, abstractproperty
from Formulas import distance


class Atom(ABC):

    def __init__(self, c=[None, None, None]):
        """
        ABC For all atoms. x, y, z are the coords over time
        """
        self.x = c[0]
        self.y = c[1]
        self.z = c[2]

    @abstractmethod
    def __str__(self):
        pass

    def update_coords(self, c):
        """
        Updates Coords to x, y, z
        :param c: Coords to Update
        :return: None
        """
        self.x = c[0]
        self.y = c[1]
        self.z = c[2]

    def current_pos(self):
        return [self.x, self.y, self.z]


class Proton(Atom):

    def __init__(self, c=[None, None, None]):
        self.atom = None
        super().__init__(c=c)

    def set_atom(self, atom):
        """
        :param atom: Any Atom
        :return: None
        """
        self.update_coords(atom.current_pos())
        self.atom = atom

    def __str__(self):
        atom_name = 'Proton'
        if self.x is not None and self.y is not None and self.z is not None:
            return 'This {} is attached to: {}'.format(atom_name, self.x, self.y, self.z, self.atom)
        return 'This is {} at (Unknown Coords)'.format(atom_name)


class Hydrogen(Atom):

    def __init__(self, c=[None, None, None], home=None, distance_to_home=0):
        """
        Represents All Hydrogen atoms
        :param home (Optional): Oxygen atom that the Hydrogen is within one unit of. If no such atom exists, is None
        """
        super().__init__(c=c)
        self.home = home
        self.distance_to_home = distance_to_home

    def find_home(self, ox_list):
        for ox in ox_list.atom_list:
            dist = distance(self.current_pos(), ox.current_pos())
            if dist < 1.005:
                self.home = ox
                self.distance_to_home = dist
                return ox
        self.home = None
        self.distance_to_home = 0
        return None

    def __str__(self):
        atom_name = 'Hydrogen'
        if self.x is not None and self.y is not None and self.z is not None:
            return 'This is {} atom at ({}, {}, {})'.format(atom_name, self.x, self.y, self.z)
        return 'This is {} atom at (Unknown Coords)'.format(atom_name)


class Oxygen(Atom):

    def __init__(self, c=[None, None, None]):
        super().__init__(c=c)

    def __str__(self):
        atom_name = 'Oxygen'
        if self.x is not None and self.y is not None and self.z is not None:
            return 'This is {} atom at ({}, {}, {})'.format(atom_name, self.x, self.y, self.z)
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
            # print(atom, " Was not added to :", self)
            pass

    def make_hydrogen_list(self):
        """
        :return: A Hydrogen list
        """
        hl = HydrogenList()
        for atom in self.atom_list:
                hl.add_atom(atom)
        return hl

    def make_oxygen_list(self):
        """
        :return: An Oxygen List
        """
        oxl = OxygenList()
        for atom in self.atom_list:
            oxl.add_atom(atom)
        return oxl


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


