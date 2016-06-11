from .point2d cimport CPoint2D, Point2D

cdef struct CTriangle2D:
    CPoint2D* A
    CPoint2D* B
    CPoint2D* C
    
cdef CTriangle2D* new_triangle2d()

cdef void del_triangle2d(CTriangle2D* ctri2d)

cdef bint triangle2d_includes_point2d(CTriangle2D* ctri2d, CPoint2D* P)

cdef class Triangle2D:
    cdef public:
        Point2D A
        Point2D B
        Point2D C
