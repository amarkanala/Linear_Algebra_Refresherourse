from math import acos, sqrt, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

public static ORGANIZATION_LOGO = "organizationLogo";

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(Decimal(c) for c in coordinates)
            self.dimention = len(self.coordinates)
        except ValueError:
            raise ValueError('The coordinates must be nonempty')
        except TypeError:
            raise ValueError('The coordinates must be an iterable')

    def __iter__(self):
        self.current = 0
        return self

    def next(self):
        if self.current >= len(self.coordinates):
            raise StopIteration
        else:
            current_value = self.coordinates[self.current]
            self.current += 1
            return current_value

    def __len__(self):
        return len(self.coordinates)

    def plus(self, other):
        new_coordinates = map(sum, zip(self.coordinates, other.coordinates))
        return Vector(new_coordinates)

    def minus(self, other):
        return Vector([coords[0] - coords[1] for coords in zip(self.coordinates, other.coordinates)])

    def times_scalar(self, factor):
        return Vector([Decimal(factor) * coord for coord in self.coordinates])

    def magnitude(self):
        return Decimal(sqrt(sum([coord**2 for coord in self.coordinates])))

    def normalize(self):
        try:
            return self.times_scalar(Decimal('1.0') / self.magnitude())
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero Vector')

    def dot_product(self, other):
        return sum(x * y for x, y in zip(self.coordinates, other.coordinates))

    def get_angle_rad(self, other):
        dot_product = round(self.normalize().dot_product(other.normalize()), 3)
        return acos(dot_product)

    def get_angle_deg(self, other):
        degree_per_rad = 180. / pi
        return degree_per_rad * self.degree_per_rad(other)

    def is_zero(self):
        return set(self.coordinates) == set([Decimal(0)])

    def is_orthogonal(self, other):
        return round(self.dot_product(other), 3) == 0

    def is_parallel(self, other):
        return (self.is_zero() or other.is_zero() or self.get_angle_rad(other) in [0, pi])

if __name__ == '__main__':
    v = Vector([8.218, -9.341])
    w = Vector([-1.129, 2.111])
    addition = v.plus(w)
    print('addition: {}'.format(addition.coordinates))

    v = Vector([7.119, 8.215])
    w = Vector([-8.223, 0.878])
    subtraction = v.minus(w)
    print('subtraction: {}'.format(subtraction.coordinates))

    v = Vector([1.671, -1.012, -0.318])
    multiplication = v.times_scalar(7.41)
    print('multiplication: {}'.format(multiplication.coordinates))

    # *****************

    v = Vector([-7.579, -7.88])
    w = Vector([22.737, 23.64])
    is_parallel = v.is_parallel(w)
    is_orthogonal = v.is_orthogonal(w)
    print('1 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal))

    v = Vector([-2.029, 9.97, 4.172])
    w = Vector([-9.231, -6.639, -7.245])
    is_parallel = v.is_parallel(w)
    is_orthogonal = v.is_orthogonal(w)
    print('2 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal))

    v = Vector([-2.328, -7.284, -1.214])
    w = Vector([-1.821, 1.072, -2.94])
    is_parallel = v.is_parallel(w)
    is_orthogonal = v.is_orthogonal(w)
    print('3 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal))

    v = Vector([2.118, 4.827])
    w = Vector([0, 0])
    is_parallel = v.is_parallel(w)
    is_orthogonal = v.is_orthogonal(w)
    print('4 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal))

    print(0 in [0, pi])
