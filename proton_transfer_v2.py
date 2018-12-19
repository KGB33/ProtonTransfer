from xyz import read_xyz


def main():
    file_name = 'h5o2_2cc_scan_sum'
    from_file_path = 'data/' + file_name + '.xyz'
    all_steps = []
    with open(from_file_path) as file:
        while True:
            try:
                all_steps.append(read_xyz(file))
            except ValueError:
                print('End of File')
                break
        coord_one = all_steps[0].coords[1]
        print(coord_one)


if __name__ == '__main__':
    main()
