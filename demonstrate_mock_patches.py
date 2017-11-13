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
    Example of how unittest.mock.patch can be used to replace the behaviour of
    a method.
    """

    def test_compute_with_patch_foo(self):
        """
        Demonstrate patching a function within a module, and
        specifying an alternate return value.
        """

        print("\nrunning test_compute_with_patch...")

        # note how this patch is used with a context manager so as to
        # restore the initial state after use
        with unittest.mock.patch('__main__.MyClassA.foo',
                                 new=Mock(return_value=500)):
            a = MyClassA()
            result = a.compute()

            self.assertEqual(result, 1200)

    # demonstrate patching using decorators
    @unittest.mock.patch('__main__.MyClassA.foo2')
    def test_compute_with_patch_foo2(self, mock_foo2):
        """
        Under this setup, when MyClassA.foo2 is called a call to the mock
        object returned by the decorator (which is now the second argument
        in the method argument list) will be made instead.

        Note how we now need to explicitly set the return value of the mock
        object below; contrast this with the context manager approach above.
        """

        mock_foo2.return_value = 750

        a = MyClassA()
        result = a.compute()

        self.assertEqual(result, 850)

    # demonstrate the order in which patch decorators are applied
    @unittest.mock.patch('__main__.MyClassA.foo2')
    @unittest.mock.patch('__main__.MyClassA.foo')
    def test_compute_with_patch_foo_and_foo2(self, mock_foo, mock_foo2):
        """
        Note the order in which decorators apply, i.e. effectively in reverse
        order with the first decorator corresponding to the last method
        argument and so on.
        """

        mock_foo.return_value = 'a'
        mock_foo2.return_value = 'b'

        a = MyClassA()
        result = a.compute()

        self.assertEqual(result, 'ab')


if __name__ == "__main__":
    unittest.main()
