import unittest
import os
import for_unittest


class MyCalcTest(unittest.TestCase):

    def test_add(self):
        c = for_unittest.add(20, 10)
        self.assertEqual(c, 30)

    def test_substract(self):
        c = for_unittest.substract(20, 10)
        self.assertEqual(c, 10)


class MyUtilTest(unittest.TestCase):

    testfile = 'test.txt'

    # run before stating unittest
    def setUp(self):
        f = open(MyUtilTest.testfile, 'w')
        f.write('1234567890')
        f.close()

    # run after end the unittest
    def tearDown(self):
        try:
            os.remove(MyUtilTest.testfile)
        except:
            pass

    def test_filelen(self):
        leng = for_unittest.filelen(MyUtilTest.testfile)
        self.assertEqual(leng, 10)

    def test_count_in_file(self):
        cnt = for_unittest.count_in_file(MyUtilTest.testfile, '0')
        self.assertEqual(cnt, 1)


if __name__ == '__main__':
    unittest.main()
