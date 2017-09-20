from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, v):
        if type(v) != Vector:
            raise TypeError('The argument must be of type Vector')

        if len(v.coordinates) != len(self.coordinates):
            raise ValueError('Cannot add vectors with different dimensions')

        new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def __sub__ (self, v):
        if type(v) != Vector:
            raise TypeError('The argument must be of type Vector')

        if len(v.coordinates) != len(self.coordinates):
            raise ValueError('Cannot subtract vectors with different dimensions')

        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def scale (self, c):
        new_coordinates = [x * Decimal(c) for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude (self):
        return Decimal(sqrt(sum([x**2 for x in self.coordinates])))

    def normalize (self):
        try:
            return self.scale(Decimal('1.0') / self.magnitude())

        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def dot_product (self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def angle_rad (self, v):
        try:
            u1 = self.normalize()
            u2 = v.normalize()
            return acos(round(u1.dot_product(u2), 3))

        except ZeroDivisionError:
            raise Exception('Cannot calculate angle with the zero vector')

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def angle_deg (self, v):
        return degrees(self.angle_rad(v))

    def is_parallel (self, v):
        return (self.is_zero()
                or v.is_zero()
                or self.angle_rad(v) == 0
                or self.angle_rad(v) == pi)

    def is_orthogonal (self, v, tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance
