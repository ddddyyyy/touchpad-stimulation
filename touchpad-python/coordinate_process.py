import argparse
import show_img


# 最简单的自定义异常
class TError(Exception):
    pass


def cluster(np):
    """
    分簇
    :param np: 电容值数组
    :return: 分簇之后的得到的点的数组
    """
    if len(np) < 1:
        return []
    temp = 0
    for i in np:
        temp += i
    avg = temp / len(np)  # 这里以数组的平均值当阈值
    is_inc = 1
    flag = 0  # 为2开始计算极大值
    total = 0  # 当前簇的加权总量
    total_p_value = 0  # 当前簇的总电容量
    result = []
    for i in range(len(np)):
        if flag == 2:
            result.append(total / total_p_value - 1)
            flag = 0
            total_p_value = 0
            total = 0
        total += np[i] * (i + 1)
        total_p_value += np[i]
        # 处理最后一个遍历到的值
        if i == len(np) - 1:
            # 如果是递增且大于阈值，或者是递减且flag为1，则开始计算极大值的位置
            if 1 == is_inc and np[i] > avg:
                # 排除最后有极大值的情况
                result.append(i)
            elif 0 == is_inc and flag == 1:
                result.append(total / total_p_value - 1)
            break
        # 值的增长方向改变
        if np[i] < np[i + 1]:
            if flag == -1:
                total_p_value = 0
                total = 0
            if 0 == is_inc:
                flag += 1
            is_inc = 1
        if np[i] > np[i + 1]:
            if 1 == is_inc:
                if i == 0:
                    # 排除一开始就有极大值的情况
                    if np[i] > avg:
                        result.append(i)
                        flag -= 1
                else:
                    # 低于阈值则不计算极大值，并将flag-1，抵消之后的递减序列
                    if np[i] > avg:
                        flag += 1
                    else:
                        flag -= 1
            is_inc = 0
    return result


def coordinate_interpolation(x, y):
    """
    坐标定位
    :param x:x轴上的np值
    :param y:y轴上的np值
    :return: 推算出来的坐标列表
    """
    x_c = cluster(x)
    y_c = cluster(y)
    result = []
    for _x in x_c:
        for _y in y_c:
            # 得到x和y值
            result.append((_x, _y))
    return result


def cal_len(coords):
    """
    计算四个或者两个坐标中最长的一条线
    :param coords:坐标列表
    :return:最长的一条线的长度
    """
    max_len = -1
    for i in range(len(coords)):
        j = i + 1
        while j < len(coords):
            t_x = coords[i][0] - coords[j][0]
            t_y = coords[i][1] - coords[j][1]
            t = t_x * t_x + t_y * t_y
            max_len = max(max_len, t)
            j += 1
    return max_len


def zoom(x1, y1, x2, y2):
    """
    判断zoom
    :param x1:第一帧的x上的np值
    :param y1:第一帧的y上的np值
    :param x2:第二帧的x上的np值
    :param y2:第二帧的y上的np值
    """
    c_c_1 = coordinate_interpolation(x1, y1)
    c_c_2 = coordinate_interpolation(x2, y2)
    # 符合zoom的条件，即判断出来的点为两个或者四个
    if (len(c_c_1) == 2 or len(c_c_1) == 4) and (len(c_c_2) == 2 or len(c_c_2) == 4):
        # 通过分别算出坐标中距离最远的点的长度进行比较，可以得出zoom的情况
        coord_1_len = cal_len(c_c_1)
        coord_2_len = cal_len(c_c_2)
        if coord_1_len > coord_2_len:
            return 'zoom in'
        elif coord_1_len < coord_2_len:
            return 'zoom out'
        else:
            return 'no change'
    else:
        return 'error input'


def input_data(prefix, debug=False):
    """
    数组输入
    :param prefix: 文本前缀
    :param debug: 是否为debug模式
    :return: 电容值数组
    """
    coord_list = []
    while True:
        try:
            input_array = input('%s电容数组(5~14个):' % prefix)
            coord_list = [int(i) for i in input_array.split(',')]
        except Exception as e:
            if e is KeyboardInterrupt:
                exit(1)
            print('输入有误，请重新输入')

        if 4 < len(coord_list) < 15:
            break
        else:
            print('请输5~14个数字')
            if debug:
                raise TError

    return coord_list


def switch(mode, debug=False):
    if mode == 1:
        print('坐标定位,请输入两列电容值列表,用逗号隔开每个元素')
        x_list = input_data('x轴的', debug)
        y_list = input_data('y轴的', debug)
        show_img.coordinate_interpolation_show(x_list, y_list, str(coordinate_interpolation(x_list, y_list)))

    elif mode == 2:
        print('分簇展示,请输入电容值列表,用逗号隔开每个元素')
        np_list = input_data('', debug)
        show_img.cluster_show(np_list, str(cluster(np_list)))
    elif mode == 3:
        print('zoom展示，请输入四列电容值列表,用逗号隔开每个元素')
        while True:
            x_list_1 = input_data('第一组x轴的', debug)
            y_list_1 = input_data('第一组y轴的', debug)
            while True:
                x_list_2 = input_data('第二组x轴的', debug)
                if len(x_list_2) != len(x_list_1):
                    print('第二组x轴的电容数组和第一组x轴的电容数组的数目不一致，请重新输入')
                    if debug:
                        raise TError
                else:
                    break
            while True:
                y_list_2 = input_data('第二组y轴的', debug)
                if len(y_list_2) != len(y_list_1):
                    print('第二组y轴的电容数组和第一组y轴的电容数组的数目不一致，请重新输入')
                    if debug:
                        raise TError
                else:
                    break

            show_img.zoom_show(x_list_1, y_list_1, x_list_2, y_list_2, zoom(x_list_1, y_list_1, x_list_2, y_list_2))
    else:
        print('非法输入')


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', metavar='程序计算的坐标模式,默认为1', type=int, required=True, default=1,
                        help='1为坐标定位，2为分簇，3为zoom检测')
    try:
        # 参数解析
        args = parser.parse_args()
        mode = args.i
        switch(mode)
    except argparse.ArgumentError:
        parser.print_help()


if __name__ == '__main__':
    start()
