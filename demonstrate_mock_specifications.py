import unittest
from unittest.mock import Mock, call


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
    Example of how unittest.mock objects can be provided with a specification to
    ensure that they only test attributes that actually exist.
    """

    @unittest.mock.patch('__main__.MyClassA')
    def test_compute_without_specification(self, mock_MyClassA):
        """
        Demonstrate mocking a class method WITHOUT a specification.
        
        Note the method 'foo3' does not exist in the specification.
        """

        a = MyClassA()

        a.foo3()

        mock_MyClassA.return_value.foo3.assert_called()

    @unittest.mock.patch('__main__.MyClassA', autospec=True)
    def test_compute_with_specification(self, mock_MyClassA):
        """
        Demonstrate mocking a class method WITH a specification.
        
        Note the method 'foo3' does not exist in the specification.
        
        In this test case, we have passed the argument 'autospec=True' into the
        function decorator. This automatically sets the mock object specication
        to the class being replaced, i.e. we can only call methods/attributes
        on the mock object that have a counterpart in the real object.
        """

        a = MyClassA()

        a.foo3()
    
        # this assertion is deliberately designed to fail
        mock_MyClassA.return_value.foo3.assert_called()


if __name__ == "__main__":
    unittest.main()
