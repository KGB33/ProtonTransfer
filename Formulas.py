import numpy as np


def distance(cord_1, cord_2):
    sum_squares = 0
    for i, j in zip(cord_1, cord_2):
        sum_squares += pow(i - j, 2)
    return np.sqrt(sum_squares)

