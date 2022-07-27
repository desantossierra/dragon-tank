import unittest

from dragon.utils.math import circumferences_intersection, two_point_angle


class TestMath(unittest.TestCase):
    def test_circumferences_intersection(self):
        output = circumferences_intersection((0, 0), 3, (3, 4), 4)
        self.assertSetEqual(set(output), {(3., 0.), (-0.84, 2.88)})

    def test_two_point_angle(self):
        self.assertEqual(two_point_angle((0, 0), (1, 0)), 0.)
        self.assertEqual(two_point_angle((0, 0), (0, 1)), 90.)
        self.assertEqual(two_point_angle((0, 0), (1, 1)), 45.)
        self.assertEqual(two_point_angle((0, 0), (-1, 0)), 180.)



if __name__ == '__main__':
    unittest.main()
