from libc.stdlib cimport malloc, free

from .polygon2d cimport CPolygon2D
from ..inclusion cimport polygon2d_winding_point2d
from .point2d cimport c_is_left

cdef CTriangle2D* new_triangle2d():
    return <CTriangle2D*> malloc(sizeof(CTriangle2D))

cdef void del_triangle2d(CTriangle2D* ctri2d):
    if ctri2d is not NULL:
        free(ctri2d)

cdef bint triangle2d_includes_point2d(CTriangle2D* ctri2d, CPoint2D* P):
    """
    inclusion.winding.polygon2d_winding_point2d specialized for triangle,
    just for optimisation.
    """
    cdef:
        int winding_number = 0

    # [AB]
    if ctri2d.A.y <= P.y:
        if ctri2d.B.y > P.y and c_is_left(ctri2d.A, ctri2d.B, P) > 0:
            winding_number +=  1
    elif ctri2d.B.y <= P.y and c_is_left(ctri2d.A, ctri2d.B, P) < 0:
        winding_number -=  1

    # [BC]
    if ctri2d.B.y <= P.y:
        if ctri2d.C.y > P.y and c_is_left(ctri2d.B, ctri2d.C, P) > 0:
            winding_number +=  1
    elif ctri2d.C.y <= P.y and c_is_left(ctri2d.B, ctri2d.C, P) < 0:
        winding_number -=  1

    # [CA]
    if ctri2d.C.y <= P.y:
        if ctri2d.A.y  > P.y and c_is_left(ctri2d.C, ctri2d.A, P) > 0:
            winding_number +=  1
    elif ctri2d.A.y <= P.y and c_is_left(ctri2d.C, ctri2d.A, P) < 0:
        winding_number -=  1

    return winding_number != 0

cdef class Triangle2D:
            
    def __init__(self, Point2D A, Point2D B, Point2D C):
        self.A = A
        self.B = B
        self.C = C

    def includes_point(Triangle2D self, Point2D point):
        cdef:
            CTriangle2D ctri2d
        ctri2d.A = self.A.cpoint2d
        ctri2d.B = self.B.cpoint2d
        ctri2d.C = self.C.cpoint2d

        return triangle2d_includes_point2d(&ctri2d, point.cpoint2d)