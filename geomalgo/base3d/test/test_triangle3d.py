import unittest

from geomalgo import Point3D, Triangle3D

class TestTriangle(unittest.TestCase):

    def test_create_triangle(self):
        A = Point3D(0,0,0)
        B = Point3D(0,1,0)
        C = Point3D(1,0,0)

        triangle = Triangle3D(A,B,C)
        self.assertEqual(triangle.B.y, 1)

        triangle.B.y = 3
        self.assertEqual(triangle.B.y, 3)

        triangle.B = Point3D(-1, -2, -3)
        self.assertEqual(triangle.B.y, -2)

    def test_area(self):
        A = Point3D(0,0,2)
        B = Point3D(0,1,2)
        C = Point3D(1,0,2)

        triangle = Triangle3D(A,B,C)
        self.assertEqual(triangle.area, 0.5)

    def test_symetric_point(self):
        A = Point3D(0,0,0)
        B = Point3D(0,1,0)
        C = Point3D(1,0,0)
        triangle = Triangle3D(A,B,C)

        P = Point3D(1,2,-3)

        S = triangle.symetric_point(P)

        self.assertEqual(S.x, 1)
        self.assertEqual(S.y, 2)
        self.assertEqual(S.z, 3)

if __name__ == '__main__':
    unittest.main()