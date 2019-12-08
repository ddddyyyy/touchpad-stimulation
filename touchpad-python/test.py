import io
import sys
import unittest

import numpy as np

import coordinate_process
import show_img


def stub_stdin(test_case_inst, inputs):
    stdin = sys.stdin

    def cleanup():
        sys.stdin = stdin

    test_case_inst.addCleanup(cleanup)
    sys.stdin = io.StringIO(inputs)


def stub_stdout(test_case_inst):
    stderr = sys.stderr
    stdout = sys.stdout

    def cleanup():
        sys.stderr = stderr
        sys.stdout = stdout

    test_case_inst.addCleanup(cleanup)
    sys.stderr = io.StringIO()
    sys.stdout = io.StringIO()


class MyTestCase(unittest.TestCase):

    def test_input(self):
        """
        边界测试
        """
        # 非法个数输入
        stub_stdout(self)
        stub_stdin(self, '1,2,3,4\n')
        self.assertRaises(coordinate_process.TError, coordinate_process.input_data, '', True)
        self.assertEqual(str(sys.stdout.getvalue()), '电容数组(5~14个):请输5~14个数字\n')
        # 非法输入
        stub_stdout(self)
        stub_stdin(self, ',,,,\n')
        self.assertRaises(coordinate_process.TError, coordinate_process.input_data, '', True)
        self.assertEqual(str(sys.stdout.getvalue()), '电容数组(5~14个):输入有误，请重新输入\n请输5~14个数字\n')

    def test_cluster(self):
        """
        分簇测试
        """
        # 空值
        self.assertEqual((coordinate_process.cluster([])), [])
        # 边界存在极大值
        self.assertEqual(coordinate_process.cluster([10, 20, 30, 40, 50]), [4])
        self.assertEqual(coordinate_process.cluster([50, 40, 30, 20, 10]), [0])
        # 两个簇
        self.assertEqual(coordinate_process.cluster([0, 1, 60, 39, 70, 30]), [2.38, 4.3])
        # 边界存在极大值且中间也有极大值
        self.assertEqual(coordinate_process.cluster([5, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 2, 3, 4, 5]),
                         [0, 8.32, 15])

    def test_coord_inter(self):
        """
        坐标推断测试
        """
        # 空值
        self.assertEqual(coordinate_process.coordinate_interpolation([], []), [])
        self.assertEqual(coordinate_process.coordinate_interpolation([1], []), [])
        self.assertEqual(coordinate_process.coordinate_interpolation([], [1]), [])
        # 坐标推断，正常输入
        self.assertEqual(coordinate_process.coordinate_interpolation([1, 2, 1], [1, 2, 1]), [(1, 1)])

    def test_zoom(self):
        """
        zoom测试
        """
        # 空值
        self.assertEqual(coordinate_process.zoom([], [], [], []), 'error input')
        # 非法输入，需要每一帧有2或者4个点才可以进行zoom判断
        self.assertEqual(coordinate_process.zoom([1, 2, 1], [1, 2, 1], [1, 2, 1], [1, 2, 1]), 'error input')
        #  正常输入
        self.assertEqual(coordinate_process.zoom([1, 2, 1, 1, 2, 1], [1, 2, 1], [1, 2, 1, 1, 2, 1], [1, 2, 1]),
                         'no change')

    def test_random(self):
        for i in range(5):
            x1 = np.random.randint(100, size=5)
            show_img.cluster_show(x1, str(coordinate_process.cluster(x1)))

        for i in range(5):
            x1 = np.random.randint(100, size=5)
            y1 = np.random.randint(100, size=5)
            show_img.coordinate_interpolation_show(x1, y1, str(coordinate_process.coordinate_interpolation(x1, y1)))

        for i in range(5):
            x1 = np.random.randint(100, size=5)
            y1 = np.random.randint(100, size=5)
            x2 = np.random.randint(100, size=5)
            y2 = np.random.randint(100, size=5)
            show_img.zoom_show(x1, y1, x2, y2, str(coordinate_process.zoom(x1, y1, x2, y2)))


if __name__ == '__main__':
    unittest.main()
