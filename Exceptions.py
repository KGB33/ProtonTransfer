class AtomDistanceError(Exception):
    """
    Raised When atoms are TOO far apart to make sense
    """
    pass


class DifferentDimensionsError(Exception):
    """
    raised when Two or more points are in Different spans
    """
    pass
