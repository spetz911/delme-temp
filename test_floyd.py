import unittest
import floyd_warshall
import StringIO
import sys

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.old_stdin = sys.stdin
        self.old_stdout = sys.stdout
        self.input = open("assets/onlinejudge.in")
        self.output = StringIO.StringIO()
        # override stdin and stdout
        sys.stdin = self.input
        sys.stdout = self.output


    def tearDown(self):
        self.input.close()
        self.output.close()
        sys.stdin = self.old_stdin
        sys.stdout = self.old_stdout


    def test_algorithm(self):
        floyd_warshall.main()
        contents = output.getvalue()
        output.close()



        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
