from typing import List

import numpy as np
from numbers import Number
from math import atan2, degrees, radians, sqrt


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

def two_point_distance(p0: (Number, Number), p1: (Number, Number)):
    (x0, y0) = p0
    (x1, y1) = p1
    return sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

def repulsive_force(distance, k_repulsive=1., influence_radius=30.):
    return k_repulsive * (1/distance - 1/influence_radius) / (distance**2)

def attractive_force(distance, k_attractive=1.):
    return k_attractive * (1/distance)

def calculate_forces(p0: (Number, Number), l1: List, attractive=True):
    if len(l1) == 0:
        return 0, 0
    if attractive:
        forces = [(two_point_angle(p0, p1), attractive_force(two_point_distance(p0, p1))) for p1 in l1]
    else:
        forces = [(two_point_angle(p0, p1), repulsive_force(two_point_distance(p0, p1))) for p1 in l1]
    acc_angle = 0
    acc_force = 0
    for ang, force in forces:
        acc_angle += (ang * force) if force>0 else ((ang + 180) * abs(force))
        acc_force += abs(force)
    angle = acc_angle/acc_force
    return angle, acc_force