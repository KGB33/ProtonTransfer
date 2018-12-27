from xyz import read_xyz, write_xyz
from Formulas import distance
from Exceptions import UnknownAtomError
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D graph
import matplotlib.pyplot as plt
import numpy as np
from Atoms import Hydrogen, HydrogenList, Oxygen, OxygenList, Proton


def main():
    # file_name = 'h5o2_2cc_scan_sum'  # Two Water Molecules
    file_name = 'h13o6_2_scan_sum'  # Six Water molecules
    from_file_path = 'data/' + file_name + '.xyz'
    to_file_path = 'data/' + file_name + '_with_proton_indicator.xyz'
    proton_coords = []

    # Read Files
    with open(from_file_path) as in_file, open(to_file_path, 'w') as out_file:
        while True:
            try:
                h_list = HydrogenList()
                ox_list = OxygenList()
                proton_indicator = Proton()
                data = read_xyz(in_file)
                for atom, coords in zip(data.atom_types, data.coords):
                    if atom == 'H':
                        h_list.add_atom(Hydrogen(c=coords))
                    elif atom == 'O':
                        ox_list.add_atom(Oxygen(c=coords))
                    else:
                        raise UnknownAtomError

                h_list.find_homes(ox_list)

                homeless = []
                for h in h_list.atom_list:
                    if h.home is None:
                        homeless.append(h)

                if homeless:
                    max_h = homeless[0]
                    for h in homeless:
                        if h.distance_to_home > max_h.distance_to_home:
                            max_h = h
                    proton_indicator.set_atom(max_h)

                if not homeless:
                    for ox in ox_list.atom_list:
                        residents = 0
                        for h in h_list.atom_list:
                            if h.home == ox:
                                residents += 1
                        if residents >= 3:
                            proton_indicator.set_atom(ox)
                proton_coords += [proton_indicator.current_pos()]

                # Write Data
                out_coords = []
                for i in zip(data.coords):
                    out_coords += i
                out_coords += (proton_coords[-1],)
                out_coords = np.asarray(out_coords)
                out_atom_types = data.atom_types + ['p+']
                out_title = data.title
                write_xyz(out_file, out_coords, out_title, out_atom_types)
            except ValueError:
                break
        plot_data(proton_coords)


def plot_data(proton_coords, step=1):
    # Set up plot
    fig = plt.figure()
    ax = fig.gca()

    # Add Data
    xs = [x for x in range(0, len(proton_coords), step)]
    y_p = [distance([0, 0, 0], proton_coords[x]) for x in range(0, len(proton_coords), step)]
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
