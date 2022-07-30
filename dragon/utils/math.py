import numpy as np
from numbers import Number
from math import atan2, degrees, radians


def circumferences_intersection(p0: (Number, Number), r0: Number, p1: (Number, Number), r1: Number) -> list:
    """
    It calculates the intersection of two circumferences given their center and radius.
    Args:
        - `p0`: first circle center
        - `r0`: first circle radius
        - `p1`: second circle center
        - `r1`: second circle radius
    Returns:
        intersection points in case of intersecting circumferences. None in any other case.
    """

    (x0, y0) = p0
    (x1, y1) = p1

    d = np.sqrt((x1-x0)**2 + (y1-y0)**2)

    if d > r0 + r1:      # non intersecting
        return None
    if d <= abs(r0-r1):  # One circle within other
        return None

    a = (r0**2-r1**2+d**2)/(2*d)
    h = np.sqrt(r0**2-a**2)
    x2 = x0+a*(x1-x0)/d
    y2 = y0+a*(y1-y0)/d
    x3 = x2+h*(y1-y0)/d
    y3 = y2-h*(x1-x0)/d

    x4 = x2-h*(y1-y0)/d
    y4 = y2+h*(x1-x0)/d

    return [(round(x3, 5), round(y3, 5)),
            (round(x4, 5), round(y4, 5))]


def circumferences_intersection_safe(p0: (Number, Number), r0: Number, p1: (Number, Number), r1: Number) -> list:
    points = circumferences_intersection(p0, r0, p1, r1)
    points = [(x,y) for (x, y) in points if y >= 0]
    return points


def two_point_angle(p0: (Number, Number), p1: (Number, Number), in_degrees: bool = True) -> Number:
    """
    It calculates the angle between two points
    Args:
        - `p0`: first point
        - `p1`: second point
        - `in_degrees`: if True, result in degrees, otherwise in radians.
    Returns:
        degrees or radians between two points
    """

    (x0, y0) = p0
    (x1, y1) = p1

    angle = atan2(y1 - y0, x1 - x0)

    if in_degrees:
        return degrees(angle)

    return radians(angle)
