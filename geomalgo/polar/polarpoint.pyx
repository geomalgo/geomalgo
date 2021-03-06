from libc.math cimport sin, cos

from ..base2d.point2d cimport Point2D

cdef class PolarPoint:

    def __init__(self, r, theta):
        self.r = r
        self.theta = theta

    def to_cartesian(self):
        cdef:
            double x
            double y
        x = self.r * cos(self.theta)
        y = self.r * sin(self.theta)
        return Point2D(x,y)

