from enum import Enum
from PIL import Image
from enum import IntEnum

MAX_X_RES = 280
MAX_Y_RES = 360
MAX_PADDING_LEFT = 30
MAX_PADDING_RIGHT = 0


class Command(Enum):
    PEN_UP = 0
    PEN_DOWN = 1
    PEN_RIGHT = 2
    PEN_LEFT = 3
    SCROLL = 4


class PixelSize(IntEnum):
    PIXEL_1x1 = 1
    PIXEL_2x2 = 2
    PIXEL_4x4 = 4


def binarized_image_to_p_codes(binarized, x_res, y_res, padding_left):
    p_codes = []
    rows = int(y_res)
    cols = int(x_res)

    p_codes.append([Command.PEN_RIGHT, padding_left])
    for i in range(rows):
        prev = binarized[i * cols]

        if prev:
            p_codes.append([Command.PEN_DOWN, 1])
        p_codes.append([Command.PEN_RIGHT, 0])

        for j in range(1, cols):
            curr = binarized[i * cols + j]
            if curr == prev:
                p_codes[-1][1] += 1
            else:
                if curr:
                    p_codes[-1][1] += 1
                    p_codes.append([Command.PEN_DOWN, 1])
                    p_codes.append([Command.PEN_RIGHT, 0])
                else:
                    p_codes.append([Command.PEN_UP, 1])
                    p_codes.append([Command.PEN_RIGHT, 0])
                    p_codes[-1][1] += 1

            prev = curr

        if len(p_codes) > 1 and p_codes[-2][0] == Command.PEN_DOWN:
            p_codes.append([Command.PEN_UP, 1])

        p_codes.append([Command.PEN_LEFT, x_res - 1 + padding_left])
        p_codes.append([Command.PEN_RIGHT, padding_left])
        p_codes.append([Command.SCROLL, 1])

    return p_codes


def binarize_image(path, x_res, y_res):
    img = Image.open(path).convert('1')

    ratio = min(x_res / img.width, y_res / img.height)
    img_x = int(img.width * ratio)
    img_y = int(img.height * ratio)
    print("{} {} x {} resized to {} x {}".format(path, img.width, img.height, img_x, img_y))
    img = img.resize((img_x, img_y))
    pixels = list(img.getdata())
    return list(map(lambda val: not val, pixels)), img_x, img_y


def generate_and_binarize_test_image(pixel_size):
    x_res = MAX_X_RES // int(pixel_size)

    binarized = ([1 for _ in range(x_res * 2)] + [0 for _ in range(x_res * 2)]) * 10  # 40 rows

    t = [[1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
         [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
         [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
         [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]

    for i in range(2):  # 22 rows
        for x in t:
            binarized.extend(x * (8 // int(pixel_size)) + [0] * (24 // int(pixel_size)))

        binarized.extend([0] * x_res)

    for j in range(14):  # 28 rows
        binarized.extend([1 if (i % 2 == 0) else 0 for i in range(x_res)])
        binarized.extend([0 if (i % 2 == 0) else 1 for i in range(x_res)])

    return list(map(bool, binarized)), x_res, 90


def generate_and_binarize_calibration_test_image(pixel_size):
    x_res = MAX_X_RES // int(pixel_size)

    binarized = ([1 for _ in range(x_res * 2)] + [0 for _ in range(x_res * 2)]) * 3  # 12 rows

    return list(map(bool, binarized)), x_res, 12
