from PIL import Image  # 导入pillow库下的image模块，主要用于图片缩放、图片灰度化、获取像素灰度值
import ctypes

def grayscale_Image(image, resize_width=9, resize_heith=8):  # image为图片的路径，resize_width为缩放图片的宽度，resize_heith为缩放图片的高度
    im = Image.open(image)  # 使用Image的open方法打开图片
    smaller_image = im.resize((resize_width, resize_heith))  # 将图片进行缩放
    grayscale_image = smaller_image.convert('L')  # 将图片灰度化
    return grayscale_image


def hash_String(image, resize_width=9, resize_heith=8):
    hash_string = ""  # 定义空字符串的变量，用于后续构造比较后的字符串
    pixels = list(grayscale_Image(image, resize_width, resize_heith).getdata())
    # 上一个函数grayscale_Image()缩放图片并返回灰度化图片，.getdata()方法可以获得每个像素的灰度值，使用内置函数list()将获得的灰度值序列化
    for row in range(1, len(pixels) + 1):  # 获取pixels元素个数，从1开始遍历
        if row % resize_width:  # 因不同行之间的灰度值不进行比较，当与宽度的余数为0时，即表示当前位置为行首位，我们不进行比较
            if pixels[row - 1] > pixels[row]:  # 当前位置非行首位时，我们拿前一位数值与当前位进行比较
                hash_string += '1'  # 当为真时，构造字符串为1
            else:
                hash_string += '0'  # 否则，构造字符串为0
        # 最后可得出由0、1组64位数字字符串，可视为图像的指纹
    return ctypes.c_int64(int(hash_string, 2)).value  # 把64位数当作2进制的数值并转换成十进制数值


def Difference(dhash1, dhash2):
    difference = dhash1 ^ dhash2  # 将两个数值进行异或运算
    return bin(difference).count('1')  # 异或运算后计算两数不同的个数，即个数<5，可视为同一或相似图片


if __name__ == '__main__':
    image1 = "/Users/fujie/PycharmProjects/相册系统/facePhoto/static/facePhoto/1588612529.808869-IMG_20190505_185644.jpg"
    image2 = "/Users/fujie/PycharmProjects/相册系统/facePhoto/static/facePhoto/1588612529.808869-IMG_20190505_185644.jpg"
    print(Difference(hash_String(image1), hash_String(image2)))
