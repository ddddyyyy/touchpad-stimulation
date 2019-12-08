from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']


# 灰度图的色值
def value(_x, _y): return - (_x + _y)


def format_array(x_list, y_list):
    string = ''
    for _y in y_list:
        for _x in x_list:
            string += '(%-3s,%-3s),' % (_x, _y)
        string = string[:-1] + '\n'
    return string


def cluster_show(np_list, result):
    """
    分簇显示
    :param np_list: 电容值列表
    :param result: 结果
    """
    plt.subplot(2, 1, 1)
    X, Y = np.meshgrid(np_list, [0])  # 生成二维数组
    imshow(value(X, Y), cmap='Blues_r')  # 生成灰度图
    plt.subplot(2, 1, 2)
    axis('off')
    text(0, 0, '分簇结果为 ' + result)
    show()


def zoom_show(x1, y1, x2, y2, result):
    X1, Y1 = np.meshgrid(x1, y1)
    X2, Y2 = np.meshgrid(x2, y2)

    plt.subplot(2, 2, 1)
    imshow(value(X1, Y1), cmap='Blues_r')
    plt.subplot(2, 2, 2)
    imshow(value(X2, Y2), cmap='Blues_r')

    subplot(2, 2, 3)
    axis('off')
    text(0, 0, (format_array(x1, y1)) + '\n' + '结果为 ' + result)

    subplot(2, 2, 4)
    axis('off')
    text(0, 0, (format_array(x2, y2)) + '\n')

    show()


def coordinate_interpolation_show(x, y, result):
    X, Y = np.meshgrid(x, y)
    plt.subplot(2, 1, 1)
    imshow(value(X, Y), cmap='Blues_r')
    plt.subplot(2, 1, 2)
    axis('off')
    text(0, 0, (format_array(x, y)) + '\n' + '结果为 ' + result)
    show()
