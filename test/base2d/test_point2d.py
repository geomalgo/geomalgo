import unittest
from math import sqrt, pi

from geomalgo import Point2D, Vector2D

class TestPoint2D(unittest.TestCase):

    def test_property_x(self):
        A = Point2D(1,2)
        self.assertEqual(A.x, 1)
        A.x = 10
        self.assertEqual(A.x, 10)

    def test_index(self):
        A = Point2D(1,2)
        self.assertEqual(A.index, 0)

        B = Point2D(1,2, index=8)
        self.assertEqual(B.index, 8)

    def test_distance(self):
        A = Point2D(2,1)
        B = Point2D(3,2)
        dist = A.distance(B)
        expected_dist = sqrt(2.)
        self.assertAlmostEqual(dist, expected_dist)

    def test_add_vector(self):
        A = Point2D(1, 2)
        v = Vector2D(3, 1)
        B = A + v
        self.assertEqual(B.x, 4)
        self.assertEqual(B.y, 3)

    def test_vector_from_point_sub_point(self):
        A = Point2D(1,2)
        B = Point2D(4,3)
        V = B - A
        self.assertEqual(V.x, 3)
        self.assertEqual(V.y, 1)

    def test_str(self):
        A = Point2D(2,1)
        expected_string = "Point2D(2.0, 1.0)"
        string = str(A)
        self.assertEqual(string, expected_string)

    def test_to_polar(self):
        A = Point2D(2, 0)
        P = A.to_polar()
        self.assertAlmostEqual(P.r, 2)
        self.assertAlmostEqual(P.theta, 0)

        A = Point2D(0, 2)
        P = A.to_polar()
        self.assertAlmostEqual(P.r, 2.)
        self.assertAlmostEqual(P.theta, pi/2)

class TestIsLeft(unittest.TestCase):

    def test_is_left(self):
        """
        P

        A----B
        """
        A = Point2D(0, 0)
        B = Point2D(1, 0)
        P = Point2D(0, 1)
        self.assertTrue(P.is_left(A,B))

    def test_is_right(self):
        """
        A----B

        P
        """
        A = Point2D(0,  0)
        B = Point2D(1,  0)
        P = Point2D(0, -1)
        self.assertFalse(P.is_left(A,B))

    def test_on_line(self):
        """
        A----B----P
        """
        A = Point2D(0, 0)
        B = Point2D(1, 0)
        P = Point2D(2, 0)
        with self.assertRaisesRegex(ValueError, "Point is on line \(AB\)"):
            P.is_left(A,B)


class TestEquality(unittest.TestCase):

    def test_equal(self):
        A = Point2D(2, 1)
        B = Point2D(2, 1)
        self.assertEqual(A, B)

    def test_not_equal(self):
        A = Point2D(1, 1)
        B = Point2D(2, 1)
        C = Point2D(1, 2)
        self.assertNotEqual(A, B)
        self.assertNotEqual(A, C)


if __name__ == '__main__':
    unittest.main()
