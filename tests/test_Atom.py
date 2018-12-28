import unittest
from Atoms import *


# setup
coords = 28
coords_two = 9


def set_coords(a, c=coords):
    a.x = c
    a.y = c
    a.z = c


o_one = Oxygen()
set_coords(o_one)

o_two = Oxygen()
set_coords(o_two, c=coords_two)

ox_list = OxygenList(o_one, o_two)

h_one = Hydrogen()
set_coords(h_one)

h_two = Hydrogen()
set_coords(h_two)

h_three = Hydrogen()
set_coords(h_three)

h_list = HydrogenList(h_one, h_two, h_three)


class TestHydrogen(unittest.TestCase):

    def test_init(self):
        h = Hydrogen()
        self.assertIsNone(h.home)

    def test_init_with_params(self):
        h = Hydrogen(c=[27.5, 28, 28], home=o_one)
        self.assertEqual(0.5, h.distance_to_closest_ox)
        self.assertEqual(o_one, h.home)

    def test_find_home(self):
        h = Hydrogen()
        set_coords(h)
        h.find_home(ox_list)
        self.assertEqual(ox_list.atom_list[0], h.home)

    def test_find_home_no_home(self):
        h = Hydrogen()
        set_coords(h, c=-3)
        h.find_home(ox_list)
        self.assertIsNone(h.home)
        
    def test_init(self):
        a = Hydrogen()
        self.assertFalse(a.z, 'The z array should be Empty')
        self.assertFalse(a.x, 'The x array should be Empty')
        self.assertFalse(a.y, 'The y array should be Empty')

    def test_update_coords(self):
        a = Hydrogen()
        a.x = coords
        a.y = coords
        a.z = coords
        self.assertEqual(coords, a.x)
        self.assertEqual(coords, a.y)
        self.assertEqual(coords, a.z)

    def test_add_coords(self):
        h = Hydrogen()
        h.update_coords([1, 2, 3])
        self.assertEqual(1, h.x)
        self.assertEqual(2, h.y)
        self.assertEqual(3, h.z)

    def test_current_pos(self):
        a = Hydrogen()
        a.x = coords
        a.y = coords
        a.z = coords
        self.assertEqual([28, 28, 28], a.current_pos())

    def test_str_no_coords(self):
        h = Hydrogen()
        self.assertEqual('This is Hydrogen atom at (Unknown Coords)', str(h))

    def test_str_with_coords(self):
        h = Hydrogen()
        set_coords(h)
        self.assertEqual('This is Hydrogen atom at (28, 28, 28)', str(h))


class TestProton(unittest.TestCase):

    def test_set_atom(self):
        p = Proton()
        p.set_atom(h_one)
        self.assertEqual(p.atom, h_one)
        self.assertEqual([28, 28, 28], p.current_pos())

    def test_str_no_coords(self):
        p = Proton()
        self.assertEqual('This is Proton at (Unknown Coords)', str(p))

    def test_str_with_coords(self):
        p = Proton()
        set_coords(p)
        self.assertEqual('This Proton is attached to: 28', str(p))


class TestOxygen(unittest.TestCase):
    
    def test_str_no_coords(self):
        ox = Oxygen()
        self.assertEqual('This is Oxygen atom at (Unknown Coords)', str(ox))

    def test_str_with_coords(self):
        ox = Oxygen()
        set_coords(ox)
        self.assertEqual('This is Oxygen atom at (28, 28, 28)', str(ox))


class TestAtomList(unittest.TestCase):

    def test_add_atom_valid_atom(self):
        a = AtomList()
        h = Hydrogen()
        a.add_atom(h)
        self.assertEqual([h], a.atom_list)

    def test_add_atom_invalid_atom(self):
        a = AtomList()
        a.add_atom([123, '456'])
        self.assertFalse(a.atom_list)

    def test_make_hydrogen_list(self):
        a = AtomList()
        a.add_atom(h_one)
        a.add_atom(h_two)
        a.add_atom(o_one)
        a.add_atom(o_two)
        self.assertEqual([h_one, h_two], a.make_hydrogen_list().atom_list)

    def test_make_oxygen_list(self):
        a = AtomList()
        a.add_atom(h_one)
        a.add_atom(h_two)
        a.add_atom(o_one)
        a.add_atom(o_two)
        self.assertEqual([o_one, o_two], a.make_oxygen_list().atom_list)


class TestHydrogenList(unittest.TestCase):

    def test_init_no_args(self):
        hl = HydrogenList()
        self.assertFalse(hl.atom_list)

    def test_init_with_good_and_bad_args(self):
        hl = HydrogenList(h_one, o_one, h_two, 123, '123', [123, '123'])
        self.assertEqual([h_one, h_two], hl.atom_list)

    def test_add_atom(self):
        hl = HydrogenList(h_one, h_two)
        hl.add_atom(h_three)
        self.assertEqual([h_one, h_two, h_three], hl.atom_list)

    def test_find_homes(self):
        n_list = NitrogenList()
        h_list.find_homes(ox_list, n_list)
        self.assertEqual(ox_list.atom_list[0], h_list.atom_list[0].home)
        self.assertEqual(ox_list.atom_list[0], h_list.atom_list[1].home)
        self.assertEqual(ox_list.atom_list[0], h_list.atom_list[2].home)


class TestOxygenList(unittest.TestCase):
    
    def test_init_no_args(self):
        oxl = OxygenList()
        self.assertFalse(oxl.atom_list)

    def test_init_with_good_and_bad_args(self):
        oxl = OxygenList(h_one, o_one, h_two, 123, '123', [123, '123'], o_two)
        self.assertEqual([o_one, o_two], oxl.atom_list)

    def test_add_atom(self):
        oxl = OxygenList(o_one)
        oxl.add_atom(o_two)
        self.assertEqual([o_one, o_two], oxl.atom_list)


if __name__ == '__main__':
    unittest.main()
