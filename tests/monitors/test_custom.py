import unittest
import operator as py_operator

from monosi.monitors.custom import Operator, Threshold


class OperatorTestSuite(unittest.TestCase):
    """ Operator test cases."""

    def test_eq_fn(self):
        op = Operator('eq')
        self.assertEqual(op.fn(), py_operator.eq)

    def test_ne_fn(self):
        op = Operator('ne')
        self.assertEqual(op.fn(), py_operator.ne)

    def test_gt_fn(self):
        op = Operator('gt')
        self.assertEqual(op.fn(), py_operator.gt)

    def test_lt_fn(self):
        op = Operator('lt')
        self.assertEqual(op.fn(), py_operator.lt)

    def test_le_fn(self):
        op = Operator('le')
        self.assertEqual(op.fn(), py_operator.le)

class ThresholdTestSuite(unittest.TestCase):
    def test_evaluate(self):
        threshold = Threshold(
            operator=Operator('lt'),
            value=99,
        )
        result = threshold.evaluate(20)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
