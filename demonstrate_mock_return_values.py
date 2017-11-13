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
    Example of how unittest.mock can be used to 're-assign' a class
    method (taking advantage of the fact that Python  functions  are
    first-class objects) and specify a return value; effectively negating the
    need to actually compute the methods directly (which in some cases may be
    prohibitivey expensive).

    Note that in practice, rather than declaring a mock object and assigning
    this to a class method / function it is more common to use a
    unittest.mock.patch.
    """

    def test_compute(self):

        # create an instance of MyClassA
        a = MyClassA()

        # create a mock object and mock methods of MyClassA
        mockObj = Mock()
        a.foo = mockObj.foo
        a.foo2 = mockObj.foo2

        # set return values for the above mocks
        a.foo.return_value = 100
        a.foo2.return_value = 300

        # run the computation; this will the mock objects above
        result = a.compute()

        # verify the result
        self.assertEqual(result, 400)

        # show some information on how the mock object is used
        test_call_list = mockObj.mock_calls
        print("\nmockObj =", test_call_list)

        # compare this against some reference calling order
        reference_call_list = [call.foo(), call.foo2(100)]
        self.assertEqual(test_call_list, reference_call_list)

        # demonstrate Mock object assert methods and properties
        self.assertTrue(mockObj.foo.called)
        mockObj.foo.assert_called()  # equivalent to above
        self.assertTrue(call.foo() in mockObj.mock_calls)  # equivalent to above
        self.assertTrue(mockObj.foo2.called)
        mockObj.foo2.assert_called()  # equivalent to above
        mockObj.foo2.assert_called_with(100)
        self.assertTrue(call.foo2(100) in mockObj.mock_calls)  # equivalent to above
        print("mockObj.foo call list =", mockObj.foo.mock_calls)
        print("mockObj.foo2 call list =", mockObj.foo2.mock_calls)


if __name__ == "__main__":
    unittest.main()
