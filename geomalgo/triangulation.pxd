from .triangulation.triangulation2d cimport (
    CTriangulation2D, new_ctriangulation2d,
    del_ctriangulation2d,Triangulation2D
)

from .triangulation.edges cimport (
    EdgeLocation, EdgeMap, BoundaryEdges, InternEdges
)
