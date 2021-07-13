from enum import Enum


class Command(Enum):
    PEN_UP = 0
    PEN_DOWN = 1
    PEN_RIGHT = 2
    PEN_LEFT = 3
    SCROLL = 4


def binarized_image_to_p_codes(binarized, x_res, y_res):
    p_codes = []
    rows = int(y_res)
    cols = int(x_res)

    for i in range(rows):
        prev = binarized[i * cols]

        if prev:
            p_codes.append([Command.PEN_DOWN, 0])
        p_codes.append([Command.PEN_RIGHT, 0])

        for j in range(1, cols):
            curr = binarized[i * cols + j]
            if curr == prev:
                p_codes[-1][1] += 1
            else:
                if curr:
                    p_codes[-1][1] += 1
                    p_codes.append([Command.PEN_DOWN, 0])
                    p_codes.append([Command.PEN_RIGHT, 0])
                else:
                    p_codes.append([Command.PEN_UP, 0])
                    p_codes.append([Command.PEN_RIGHT, 0])
                    p_codes[-1][1] += 1

            prev = curr

        if len(p_codes) > 1 and p_codes[-2][0] == Command.PEN_DOWN:
            p_codes.append([Command.PEN_UP, 0])

        p_codes.append([Command.PEN_LEFT, x_res - 1])
        p_codes.append([Command.SCROLL, 1])

    return p_codes
