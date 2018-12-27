import numpy as np
from Exceptions import DifferentDimensionsError


def distance(cord_1, cord_2, zero_fill=True):
    """
    Calculates the Euclidean distance between two points.


    :param cord_1: (Array-like, numeric)
        Coords of First Point

    :param cord_2: (Array-like, numeric)
        Coords of Second Point

    :param zero_fill: (Optional, Boolean, (default=True)):
        The points should have the same dimensionality, ie, both in R^n,
        if they do not then There are two options:
                if Zero_Fill: (Default)
                    missing dimensionality is assumed to be zero
                else:
                    least Squares Approximation is used

    :return: (float)
        Distance between the two points

    Examples:
        distance([0], [5])) --> 5
        distance([0, 0, 0, 0], [5, 5, 5, 5]) --> 10

        distance([3, 4, 5], [0, 0]) --> 5
        distance([3, 4, 5], [0, 0], zero_fill=False) --> 5
        distance([2, 3, 6], [0, 0], zero_fill=True) --> 7
    """
    try:
        if len(cord_1) == len(cord_2):
            sum_squares = 0
            for i, j in zip(cord_1, cord_2):
                sum_squares += pow(i - j, 2)
            return np.sqrt(sum_squares)
        else:
            raise DifferentDimensionsError

    except DifferentDimensionsError:

        # uses Least Squares Approx
        if not zero_fill:
            # TODO: Switch Print Statement To logger
            print("{} and {} do not have the same dimensions. Using Least Squares Approx".format(cord_1, cord_2))
            if len(cord_1) > len(cord_2):
                return distance(cord_1[:len(cord_2)], cord_2)
            else:
                return distance(cord_1, cord_2[:len(cord_1)])

        # Assumes missing dimensions are Zero
        else:
            # TODO: Switch Print Statement To logger
            print("{} and {} do not have the same dimensions. "
                  "Assuming missing dimensions are zero".format(cord_1, cord_2))
            if len(cord_1) > len(cord_2):
                return distance(cord_1, cord_2 + [0 for _ in range(len(cord_2), len(cord_1))])
            else:
                return distance(cord_1 + [0 for _ in range(len(cord_1), len(cord_2))], cord_2)
