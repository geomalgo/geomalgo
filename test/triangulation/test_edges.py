import unittest

import numpy as np
from numpy.testing import assert_equal

from geomalgo import build_edges
from geomalgo.data import step, hole

class TestStep(unittest.TestCase):

    def setUp(self):
        self.intern_edges, self.boundary_edges = build_edges(step.trivtx,
                                                             step.NV)

        self.boundary_edges.add_label(step.boundary_edge_label)
        self.boundary_edges.compute_length(step.x, step.y)
        self.boundary_edges.compute_normal(step.x, step.y)

    def test_internal_edges_vertices(self):
        vert = np.asarray(self.intern_edges.vertices)
        self.assertEqual(vert.shape, (step.NI, 2))
        assert_equal(vert[0], (1,3))
        assert_equal(vert[1], (1,4))
        assert_equal(vert[2], (2,4))
        assert_equal(vert[3], (3,4))
        assert_equal(vert[4], (4,6))

    def test_internal_edges_triangles(self):
        tri = np.asarray(self.intern_edges.triangles)
        self.assertEqual(tri.shape, (step.NI, 2))
        assert_equal(tri[0], (0,2))
        assert_equal(tri[1], (2,1))
        assert_equal(tri[2], (1,3))
        assert_equal(tri[3], (4,2))
        assert_equal(tri[4], (4,5))

    def test_boundary_edges_vertices(self):
        vert = np.asarray(self.boundary_edges.vertices)
        self.assertEqual(vert.shape, (step.NB, 2))
        assert_equal(vert[0], (0,1))
        assert_equal(vert[1], (3,0))
        assert_equal(vert[2], (1,2))
        assert_equal(vert[3], (2,5))
        assert_equal(vert[4], (6,3))
        assert_equal(vert[5], (5,4))
        assert_equal(vert[6], (4,7))
        assert_equal(vert[7], (7,6))

    def test_boundary_edges_triangle(self):
        tri = np.asarray(self.boundary_edges.triangle)
        self.assertEqual(tri.shape, (step.NB,))
        assert_equal(tri[0], 0)
        assert_equal(tri[1], 0)
        assert_equal(tri[2], 1)
        assert_equal(tri[3], 3)
        assert_equal(tri[4], 4)
        assert_equal(tri[5], 3)
        assert_equal(tri[6], 5)
        assert_equal(tri[7], 5)

    def test_boundary_edge_next(self):
        nextbe = np.asarray(self.boundary_edges.next_boundary_edge)
        self.assertEqual(nextbe.shape, (step.NB,))
        self.assertEqual(nextbe[0], 2) # (0,1), (1,2)
        self.assertEqual(nextbe[1], 0) # (3,0), (0,1)
        self.assertEqual(nextbe[2], 3) # (1,2), (2,5)
        self.assertEqual(nextbe[3], 5) # (2,5), (5,4)
        self.assertEqual(nextbe[4], 1) # (6,3), (3,0)
        self.assertEqual(nextbe[5], 6) # (5,4), (4,7)
        self.assertEqual(nextbe[6], 7) # (4,7), (7,6)
        self.assertEqual(nextbe[7], 4) # (7,6), (6,3)

    def test_edge_map(self):
        edge_map = self.intern_edges.edge_map

        bounds = np.asarray(edge_map.bounds)
        edges = np.asarray(edge_map.edges)
        location = np.asarray(edge_map.location)
        idx = np.asarray(edge_map.idx)

        # Indices for edges.
        assert_equal(bounds, [
             0,  2, # 0
             2,  5, # 1
             6,  8, # 2
             9, 11, # 3
            13, 16, # 4
            19, 19, # 5
            21, 22, # 6
            24, 24, # 7
            26,
        ])

        assert_equal(edges, [
                     # V0    bounds  edges

            1, 3,    # 0 =>  0:2  => (0,1), (0,3)
                     # 0 =>  2:2  =>

            3, 2, 4, # 1 =>  2:5  => (1,3), (1,2), (1,4)
            0,       # 1 =>  5:6  => (1,0)

            4, 5,    # 2 =>  6:8  => (2,4), (2,5)
            1,       # 2 =>  8:9  => (2,1)

            4, 6,    # 3 =>  9:11 => (3,4), (3,6)
            1, 0,    # 3 => 11:13 => (3,1), (3,0)

            5, 6, 7, # 4 => 13:16 => (4,5), (4,6), (4,7)
            2, 1, 3, # 4 => 16:19 => (4,2), (4,1), (4,3)

                     # 5 => 19:19 =>
            2, 4,    # 5 => 19:21 => (5,2), (5,4)

            7,       # 6 => 21:22 => (6,7)
            4, 3,    # 6 => 22:24 => (6,4), (6,3)

                     # 7 => 24:24 =>
            4, 6,    # 7 => 24:26 => (7,4), (7,6)
        ])

        # Whether to use idx for boundary_edges or intern_edges
        assert_equal(location, [
                     # V0    bounds  edges

            1, 1,    # 0 =>  0:2  => (0,1), (0,3)
                     # 0 =>  2:2  =>

            0, 1, 0, # 1 =>  2:5  => (1,3), (1,2), (1,4)
            1,       # 1 =>  5:6  => (1,0)

            0, 1,    # 2 =>  6:8  => (2,4), (2,5)
            1,       # 2 =>  8:9  => (2,1)

            0, 1,    # 3 =>  9:11 => (3,4), (3,6)
            0, 1,    # 3 => 11:13 => (3,1), (3,0)

            1, 0, 1, # 4 => 13:16 => (4,5), (4,6), (4,7)
            0, 0, 0, # 4 => 16:19 => (4,2), (4,1), (4,3)

                     # 5 => 19:19 =>
            1, 1,    # 5 => 19:21 => (5,2), (5,4)

            1,       # 6 => 21:22 => (6,7)
            0, 1,    # 6 => 22:24 => (6,4), (6,3)

                     # 7 => 24:24 =>
            1, 1,    # 7 => 24:26 => (7,4), (7,6)
        ])

        # Index for boundary_edges or intern_edges
        assert_equal(idx, [
                     # V0    bounds  edges

            0, 1,    # 0 =>  0:2  => (0,1), (0,3)
                     # 0 =>  2:2  =>

            0, 2, 1, # 1 =>  2:5  => (1,3), (1,2), (1,4)
            0,       # 1 =>  5:6  => (1,0)

            2, 3,    # 2 =>  6:8  => (2,4), (2,5)
            2,       # 2 =>  8:9  => (2,1)

            3, 4,    # 3 =>  9:11 => (3,4), (3,6)
            0, 1,    # 3 => 11:13 => (3,1), (3,0)

            5, 4, 6, # 4 => 13:16 => (4,5), (4,6), (4,7)
            2, 1, 3, # 4 => 16:19 => (4,2), (4,1), (4,3)

                     # 5 => 19:19 =>
            3, 5,    # 5 => 19:21 => (5,2), (5,4)

            7,       # 6 => 21:22 => (6,7)
            4, 4,    # 6 => 22:24 => (6,4), (6,3)

                     # 7 => 24:24 =>
            6, 7,    # 7 => 24:26 => (7,4), (7,6)
        ])

    def test_label(self):
        label = self.boundary_edges.label

        self.assertEqual(label.shape, (step.NB,))
        self.assertEqual(label[0], 1) # (0,1)
        self.assertEqual(label[1], 2) # (3,0)
        self.assertEqual(label[2], 1) # (1,2)
        self.assertEqual(label[3], 2) # (2,5)
        self.assertEqual(label[4], 2) # (6,3)
        self.assertEqual(label[5], 2) # (5,4)
        self.assertEqual(label[6], 2) # (4,7)
        self.assertEqual(label[7], 3) # (7,6)

    def test_wrong_number_of_label(self):
        label_wrong_number = step.boundary_edge_label[:-1]
        msg = "7 label are given, but there are 8 boundary edges"
        with self.assertRaisesRegex(ValueError, msg):
            self.boundary_edges.add_label(label_wrong_number)

    def test_missing_label(self):
        label_missing = step.boundary_edge_label.copy()
        label_missing[0] = label_missing[-1]
        msg = "Missing label for edge \(0, 1\)"
        with self.assertRaisesRegex(ValueError, msg):
            self.boundary_edges.add_label(label_missing)

    def test_duplicated_label(self):
        label_duplicated = step.boundary_edge_label.copy()
        label_duplicated[1] = label_duplicated[0]
        msg = "Reference for edge \(0, 1\) is given 2 times"
        with self.assertRaisesRegex(ValueError, msg):
            self.boundary_edges.add_label(label_duplicated)

    def test_length(self):
        length = np.asarray(self.boundary_edges.length)
        self.assertEqual(length.shape, (step.NB,))
        assert_equal(length[0], 1)   # (0,1)
        assert_equal(length[1], 1)   # (3,0)
        assert_equal(length[2], 1.5) # (1,2)
        assert_equal(length[3], 1)   # (2,5)
        assert_equal(length[4], 1)   # (6,3)
        assert_equal(length[5], 1.5) # (5,4)
        assert_equal(length[6], 1)   # (4,7)
        assert_equal(length[7], 1)   # (7,6)

    def test_normal(self):
        normal = np.asarray(self.boundary_edges.normal)
        self.assertEqual(normal.shape, (step.NB, 2))
        assert_equal(normal[0], ( 0, -1))  # (0,1)
        assert_equal(normal[1], (-1,  0))  # (3,0)
        assert_equal(normal[2], ( 0, -1))  # (1,2)
        assert_equal(normal[3], ( 1,  0))  # (2,5)
        assert_equal(normal[4], (-1,  0))  # (6,3)
        assert_equal(normal[5], ( 0,  1))  # (5,4)
        assert_equal(normal[6], ( 1,  0))  # (4,7)
        assert_equal(normal[7], ( 0,  1))  # (7,6)


class TestHole(unittest.TestCase):

    def setUp(self):
        self.intern_edges, self.boundary_edges = build_edges(hole.trivtx,
                                                             hole.NV)
        self.edge_map = self.intern_edges.edge_map

    def assert_intern_triangles(self, A, B, T, U):
        """Check that intern edge (A, B) has triangles (T, U)"""
        t, u = self.intern_edges[(A,B)]
        if (t, u) != (T, U):
            raise AssertionError(
                "Expected intern edge ({}, {}) to have triangles ({}, {}),"
                "but has triangles: ({}, {})" .format(T, U, t, u))

    def test_internal_edges(self):
        self.assertEqual(self.intern_edges.vertices.shape, (hole.NI, 2))
        self.assertEqual(self.intern_edges.triangles.shape, (hole.NI, 2))
        self.assert_intern_triangles( 9, 10,  8, 18)
        self.assert_intern_triangles(24, 30, 36, 37)
        self.assert_intern_triangles( 8, 15,  6, 23)

    def test_no_such_intern_edge(self):
        with self.assertRaisesRegex(KeyError, "No such intern edge"):
            self.intern_edges[(10, 18)]

    def assert_boundary_triangle(self, A, B, T):
        """Check that boundary edge (A, B) has triangles T"""
        t = self.boundary_edges[(A,B)]
        if t != T:
            raise AssertionError(
                "Expected boundary edge ({}, {}) to have triangle {},"
                "but has triangle: {}" .format(T, t))

    def test_boundary_edges(self):
        self.assertEqual(self.boundary_edges.vertices.shape, (hole.NB, 2))
        self.assertEqual(self.boundary_edges.triangle.shape, (hole.NB, ))
        self.assert_boundary_triangle( 2 , 3,  2)
        self.assert_boundary_triangle(18, 17, 25)
        self.assert_boundary_triangle(28, 21, 32)

    def test_label(self):
        self.boundary_edges.add_label(hole.boundary_edge_label)

        label = self.boundary_edges.label

        self.assertEqual(label.shape, (hole.NB,))

if __name__ == '__main__':
    unittest.main()
