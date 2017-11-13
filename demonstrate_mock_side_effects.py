import unittest
from unittest.mock import Mock


class MyClassA():

    def foo(self):
        return 100

    def foo2(self, num):
        return num + 200

    def compute(self):
        x1 = self.foo()
        x2 = self.foo2(x1)
        result = x1 + x2
        return result


class TestA(unittest.TestCase):
    """
    Example of how unittest.mock can be used to simulate side effects.

    This can be useful if a specific behaviour to be tested is desired, e.g.
    if you want to check that a method handles errors as expected (see
    examples 1 and 2 below).

    To simultaneously pass a side effect and a return value simply return the
    desired value from the side effect function (see example 3 below).
    
    Side effects can also be used to pass a list of arguments to the mocked 
    method will be returned sequentially following each call (see example 4).
    """

    def test_compute_with_side_effect_ex_1(self):
        """
        Demonstrate mocking a class method with a specified a side effect.
        """

        mockObj = Mock(side_effect=ValueError('An example ValueError'))

        a = MyClassA()
        a.foo = mockObj
        self.assertRaises(ValueError, a.compute)

    @unittest.mock.patch('__main__.MyClassA.foo2')
    def test_compute_with_side_effect_ex_2(self, mock_foo2):
        """
        A similar example but using decorators.
        """

        mock_foo2.side_effect = TypeError('An example TypeError')

        a = MyClassA()
        self.assertRaises(TypeError, a.compute)

    @unittest.mock.patch('__main__.MyClassA.compute')
    def test_compute_with_side_effect_ex_3(self, mock_compute):
        """
        A more complex example calling a dedicated side_effect function.
        """

        def side_effect():
            print('\n***Demonstrating use of side effects***')
            return 'Side effect - including return value - specified'

        mock_compute.side_effect = side_effect

        a = MyClassA()
        result = a.compute()
        self.assertEqual(result, 'Side effect - including return value - '
                                 'specified')

    @unittest.mock.patch('__main__.MyClassA.foo')
    def test_compute_with_side_effect_ex_4(self, mock_foo):
        """
        An example showing how a list of differeing arguments can be returned
        by the mock object.
        
        This can be useful to test a range of possible input values to an
        interim function, or to check a function using a sensible value, an
        upper bound edge case, and a lower bound edge case, for example.
        """

        mock_foo.side_effect = [100, 300, 500]

        a = MyClassA()
        
        self.assertEqual(a.compute(), 400)
        self.assertEqual(a.compute(), 800)
        self.assertEqual(a.compute(), 1200)


if __name__ == "__main__":
    unittest.main()
