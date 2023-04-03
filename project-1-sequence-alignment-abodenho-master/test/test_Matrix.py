import unittest
from parameterized import parameterized

from source.Matrix import *

DIR = "ressources" # must be changed when testing locally (annoying relative path in Github workflow)

class TestMat(unittest.TestCase):

    @parameterized.expand([
        [4, 5, None],
        [60, 13, 0],
    ])
    def test_properties(self, nrows, ncols, val):
        mat = Matrix(nrows, ncols, val)
        self.assertEqual(mat.get_num_rows(),nrows)
        self.assertEqual(mat.get_num_cols(), ncols)
        self.assertEqual(mat[0, 0], val)

    def test_set(self):
        mat = Matrix(10, 10, 0)
        mat.set_value(3, 5, 8)
        self.assertEqual(mat[3, 5], 8)

    def test_max(self):
        mat = Matrix(10, 10, 0)
        mat.set_value(3, 5, 8)
        mat.set_value(4, 8, 5)
        mat.set_value(6, 3, 8)
        mat.set_value(8, 7, 8)
        self.assertEqual(mat.get_max(), (3, 5, 8), msg ="It must be the closest position to the last cell of the matrix")


class TestMatSub(unittest.TestCase):
    def setUp(self):
        self.submatblosum = SubstitutionMatrix(f"{DIR}/blosum80.txt")
        self.submatpam = SubstitutionMatrix(f"{DIR}/pam120.txt")

    def test_sub_properties(self):
        self.assertEqual(self.submatblosum.get_num_rows(), 20, msg = "Don't forget to exclude the rows of B, X, Z and *")
        self.assertEqual(self.submatpam.get_num_cols(), 20, msg="Don't forget to exclude the columns of B, X, Z and *")

    @parameterized.expand([
        ['A', 'A', 5, 3],
        ['Q', 'N', 0, 0],
        ['N', 'Q', 0, 0],
        ['G', 'Y', -4, -6]
    ])
    def test_sub_score(self, a, b, scoreblosum, scorepam):
        self.assertEqual(self.submatblosum[a,b], scoreblosum)
        self.assertEqual(self.submatpam[a, b], scorepam)

if __name__ == '__main__':
    unittest.main()