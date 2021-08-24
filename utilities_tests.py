import unittest
import utilities
from parameterized import parameterized_class, parameterized
from itertools import chain

test_binarized_image_to_p_codes_data = [[
    ("1x1 1", 1, 1,
        [True],
        [
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.PEN_DOWN, 1],
            [utilities.Command.PEN_RIGHT, 0],
            [utilities.Command.PEN_UP, 1],
            [utilities.Command.PEN_LEFT, 1 - 1 + padding],
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.SCROLL, 1]
        ], padding),
    ("1x1 2", 1, 1,
        [False],
        [
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.PEN_RIGHT, 0],
            [utilities.Command.PEN_LEFT, 1 - 1 + padding],
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.SCROLL, 1]
        ], padding),
    ("2x1 1", 2, 1,
        [True, True],
        [
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.PEN_DOWN, 1],
            [utilities.Command.PEN_RIGHT, 1],
            [utilities.Command.PEN_UP, 1],
            [utilities.Command.PEN_LEFT, 2 - 1 + padding],
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.SCROLL, 1]
        ], padding),
    ("2x1 2", 2, 1,
        [True, False],
        [
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.PEN_DOWN, 1],
            [utilities.Command.PEN_RIGHT, 0],
            [utilities.Command.PEN_UP, 1],
            [utilities.Command.PEN_RIGHT, 1],
            [utilities.Command.PEN_LEFT, 2 - 1 + padding],
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.SCROLL, 1]
        ], padding),
    ("2x1 3", 2, 1,
        [False, True],
        [
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.PEN_RIGHT, 1],
            [utilities.Command.PEN_DOWN, 1],
            [utilities.Command.PEN_RIGHT, 0],
            [utilities.Command.PEN_UP, 1],
            [utilities.Command.PEN_LEFT, 2 - 1 + padding],
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.SCROLL, 1]
        ], padding),
    ("2x1 4", 2, 1,
        [False, False],
        [
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.PEN_RIGHT, 1],
            [utilities.Command.PEN_LEFT, 2 - 1 + padding],
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.SCROLL, 1]
        ], padding),
    ("2x2 1", 2, 2,
     [False, False,
      False, False],
     [
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.PEN_RIGHT, 1],
            [utilities.Command.PEN_LEFT, 2 - 1 + padding],
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.SCROLL, 1],

            [utilities.Command.PEN_RIGHT, 1],
            [utilities.Command.PEN_LEFT, 2 - 1 + padding],
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 2", 2, 2,
     [False, False,
      False, True],
     [
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.PEN_RIGHT, 1],
            [utilities.Command.PEN_LEFT, 2 - 1 + padding],
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.SCROLL, 1],
            
            [utilities.Command.PEN_RIGHT, 1],
            [utilities.Command.PEN_DOWN, 1],
            [utilities.Command.PEN_RIGHT, 0],
            [utilities.Command.PEN_UP, 1],
            [utilities.Command.PEN_LEFT, 2 - 1 + padding],
            [utilities.Command.PEN_RIGHT, padding],
            [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 3", 2, 2,
     [False, False,
      True, False],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 4", 2, 2,
     [False, False,
      True, True],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 5", 2, 2,
     [False, True,
      False, False],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 6", 2, 2,
     [False, True,
      False, True],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 7", 2, 2,
     [False, True,
      True, False],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 8", 2, 2,
     [False, True,
      True, True],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 9", 2, 2,
     [True, False,
      False, False],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 10", 2, 2,
     [True, False,
      False, True],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 11", 2, 2,
     [True, False,
      True, False],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 12", 2, 2,
     [True, False,
      True, True],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 13", 2, 2,
     [True, True,
      False, False],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 14", 2, 2,
     [True, True,
      False, True],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 15", 2, 2,
     [True, True,
      True, False],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("2x2 16", 2, 2,
     [True, True,
      True, True],
     [
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],

        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 1],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 2 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ], padding),
    ("10x10 1", 10, 10,
     [(x // 10) % 2 == 0 for x in range(10 * 10)],
        [[utilities.Command.PEN_RIGHT, padding]] + [
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 10 - 1],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_LEFT, 10 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
        [utilities.Command.PEN_RIGHT, 10 - 1],
        [utilities.Command.PEN_LEFT, 10 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1]
     ] * (10 // 2), padding),
    ("10x10 2", 10, 10,
     [x % 2 == 0 for x in range(10 * 10)],
        [[utilities.Command.PEN_RIGHT, padding]] + [
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 2],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 2],

        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 2],
        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 2],

        [utilities.Command.PEN_DOWN, 1],
        [utilities.Command.PEN_RIGHT, 0],
        [utilities.Command.PEN_UP, 1],
        [utilities.Command.PEN_RIGHT, 1],

        [utilities.Command.PEN_LEFT, 10 - 1 + padding],
        [utilities.Command.PEN_RIGHT, padding],
        [utilities.Command.SCROLL, 1],
     ] * 10, padding),
] for padding in [
    utilities.MAX_PADDING_LEFT // utilities.PixelSize.PIXEL_1x1,
    utilities.MAX_PADDING_LEFT // utilities.PixelSize.PIXEL_2x2,
    utilities.MAX_PADDING_LEFT // utilities.PixelSize.PIXEL_4x4
]]


class BinarizedImageToPCodesTests(unittest.TestCase):
    @parameterized.expand(list(chain(*test_binarized_image_to_p_codes_data)))
    def test_binarized_image_to_p_codes(self, _, x_res, y_res, binarized, expected, padding):
        self.assertEqual(expected, utilities.binarized_image_to_p_codes(binarized, x_res, y_res, padding))


@parameterized_class(("image_path", "x_res", "y_res", "multicolor", "expected_img", "expected_x", "expected_y"), [
    ("test_images/horizontal_stripes_10x10.png", 10, 10, False, [(i // 10) % 2 == 0 for i in range(100)], 10, 10),
    ("test_images/horizontal_stripes_10x10.png", 15, 10, False, [(i // 10) % 2 == 0 for i in range(100)], 10, 10),
    ("test_images/horizontal_stripes_10x10.png", 8, 7, False, [
            True, True, True, True, True, True, True,
            True, True, True, True, True, True, True,
            False, False, False, False, False, False, False,
            False, False, False, False, False, False, False,
            True, True, True, True, True, True, True,
            False, False, False, False, False, False, False,
            False, False, False, False, False, False, False], 7, 7)
])
class BinarizeSingleColorImageTests(unittest.TestCase):
    def test_binarize_image(self):
        b, x, y = utilities.binarize_image(self.image_path, self.x_res, self.y_res, self.multicolor)
        self.assertEqual(b[0], self.expected_img)
        self.assertEqual(self.expected_x, y)
        self.assertEqual(self.expected_y, y)


@parameterized_class(("image_path", "x_res", "y_res", "multicolor", "expected_img", "expected_x", "expected_y"), [
    ("test_images/multicolor_square.png", 5, 5, True, [
            [True, False, False, False, False,
             False, True, False, False, False,
             False, False, True, False, False,
             False, False, False, True, False,
             False, False, False, False, True],

            [False, False, False, True, True,
             False, False, False, False, False,
             False, False, False, False, False,
             False, False, False, False, False,
             False, False, False, False, False],

            [False, False, False, False, False,
             False, False, False, True, True,
             False, False, False, True, True,
             False, False, False, False, False,
             False, False, False, False, False],

            [False, False, False, False, False,
             True, False, False, False, False,
             True, False, False, False, False,
             True, False, False, False, False,
             False, True, True, False, False],

            [False, False, False, False, False,
             False, False, False, False, False,
             False, False, False, False, False,
             False, False, False, False, True,
             True, False, False, True, False]], 5, 5),
])
class BinarizeMultiColorImageTests(unittest.TestCase):
    def test_binarize_image(self):
        b, x, y = utilities.binarize_image(self.image_path, self.x_res, self.y_res, self.multicolor)

        for b, e in zip(b, self.expected_img):
            self.assertEqual(e, b)
        self.assertEqual(self.expected_x, x)
        self.assertEqual(self.expected_y, y)


class GenerateAndBinarizeTestImage(unittest.TestCase):
    @parameterized.expand([
        ("1x1", utilities.PixelSize.PIXEL_1x1, (280, 90)),
        ("2x2", utilities.PixelSize.PIXEL_2x2, (140, 90)),
        ("3x3", utilities.PixelSize.PIXEL_4x4, (70, 90))
    ])
    def test_generate_and_binarize_test_image(self, _, pixel_size, expected):
        binarized, img_x, img_y = utilities.generate_and_binarize_test_image(pixel_size)
        expected_x_res, expected_y_res = expected
        self.assertEqual(expected_x_res * expected_y_res, len(binarized[0]))

    @parameterized.expand([
        ("1x1", utilities.PixelSize.PIXEL_1x1, (280, 12)),
        ("2x2", utilities.PixelSize.PIXEL_2x2, (140, 12)),
        ("3x3", utilities.PixelSize.PIXEL_4x4, (70, 12))
    ])
    def test_generate_and_binarize_calibration_test_image(self, _, pixel_size, expected):
        binarized, img_x, img_y = utilities.generate_and_binarize_calibration_test_image(pixel_size)
        expected_x_res, expected_y_res = expected
        self.assertEqual(expected_x_res * expected_y_res, len(binarized[0]))


class PaletteManagement(unittest.TestCase):
    def test_rgb_to_the_closest_color_name(self):
        rgb_values = [
            (0, 0, 0),
            (0, 0, 128),
            (0, 0, 139),
            (0, 0, 205),
            (0, 0, 255),

            (0, 100, 0),
            (0, 128, 0),
            (0, 128, 128),
            (0, 139, 139),
            (0, 191, 255),

            (0, 206, 209),
            (0, 250, 154),
            (0, 255, 0),
            (0, 255, 127),
            (0, 255, 255),

            (25, 25, 112),
            (30, 144, 255),
            (32, 178, 170),
            (34, 139, 34),
            (46, 139, 87),

            (47, 79, 79),
            (50, 205, 50),
            (60, 179, 113),
            (64, 224, 208),
            (65, 105, 225),

            (70, 130, 180),
            (72, 61, 139),
            (72, 209, 204),
            (75, 0, 130),
            (85, 107, 47),

            (95, 158, 160),
            (100, 149, 237),
            (102, 51, 153),
            (102, 205, 170),
            (105, 105, 105),

            (106, 90, 205),
            (107, 142, 35),
            (112, 128, 144),
            (119, 136, 153),
            (123, 104, 238),

            (124, 252, 0),
            (127, 255, 0),
            (127, 255, 212),
            (128, 0, 0),
            (128, 0, 128),

            (128, 128, 0),
            (128, 128, 128),
            (135, 206, 235),
            (135, 206, 250),
            (138, 43, 226),

            (139, 0, 0),
            (139, 0, 139),
            (139, 69, 19),
            (143, 188, 143),
            (144, 238, 144),

            (147, 112, 219),
            (148, 0, 211),
            (152, 251, 152),
            (153, 50, 204),
            (154, 205, 50),

            (160, 82, 45),
            (165, 42, 42),
            (169, 169, 169),
            (173, 216, 230),
            (173, 255, 47),

            (175, 238, 238),
            (176, 196, 222),
            (176, 224, 230),
            (178, 34, 34),
            (184, 134, 11),

            (186, 85, 211),
            (188, 143, 143),
            (189, 183, 107),
            (192, 192, 192),
            (199, 21, 133),

            (205, 92, 92),
            (205, 133, 63),
            (210, 105, 30),
            (210, 180, 140),
            (211, 211, 211),

            (216, 191, 216),
            (218, 112, 214),
            (218, 165, 32),
            (219, 112, 147),
            (220, 20, 60),

            (220, 220, 220),
            (221, 160, 221),
            (222, 184, 135),
            (224, 255, 255),
            (230, 230, 250),

            (233, 150, 122),
            (238, 130, 238),
            (238, 232, 170),
            (240, 128, 128),
            (240, 230, 140),

            (240, 248, 255),
            (240, 255, 240),
            (240, 255, 255),
            (244, 164, 96),
            (245, 222, 179),

            (245, 245, 220),
            (245, 245, 245),
            (245, 255, 250),
            (248, 248, 255),
            (250, 128, 114),

            (250, 235, 215),
            (250, 240, 230),
            (250, 250, 210),
            (253, 245, 230),
            (255, 0, 0),

            (255, 0, 255),
            (255, 20, 147),
            (255, 69, 0),
            (255, 99, 71),
            (255, 105, 180),

            (255, 127, 80),
            (255, 140, 0),
            (255, 160, 122),
            (255, 165, 0),
            (255, 182, 193),

            (255, 192, 203),
            (255, 215, 0),
            (255, 218, 185),
            (255, 222, 173),
            (255, 228, 181),

            (255, 228, 196),
            (255, 228, 225),
            (255, 235, 205),
            (255, 239, 213),
            (255, 240, 245),

            (255, 245, 238),
            (255, 248, 220),
            (255, 250, 205),
            (255, 250, 240),
            (255, 250, 250),

            (255, 255, 0),

            (255, 255, 224),
            (255, 255, 240),
            (255, 255, 255),

            (0, 3, 12),
            (10, 10, 10),
            (20, 0, 1),

            (254, 253, 250),
            (250, 255, 255),
            (251, 254, 255),

            (255, 10, 7),
            (210, 1, 2),
            (128, 0, 0),

            (0, 240, 2),
            (10, 220, 34),
            (0, 128, 0),

            (0, 0, 250),
            (10, 10, 252),
            (20, 11, 220)
        ]

        expected_names = [
            "black",
            "navy",
            "darkblue",
            "mediumblue",
            "blue",

            "darkgreen",
            "green",
            "teal",
            "darkcyan",
            "deepskyblue",

            "darkturquoise",
            "mediumspringgreen",
            "lime",
            "springgreen",
            "cyan",

            "midnightblue",
            "dodgerblue",
            "lightseagreen",
            "forestgreen",
            "seagreen",

            "darkslategrey",
            "limegreen",
            "mediumseagreen",
            "turquoise",
            "royalblue",

            "steelblue",
            "darkslateblue",
            "mediumturquoise",
            "indigo",
            "darkolivegreen",

            "cadetblue",
            "cornflowerblue",
            "rebeccapurple",
            "mediumaquamarine",
            "dimgrey",

            "slateblue",
            "olivedrab",
            "slategrey",
            "lightslategrey",
            "mediumslateblue",

            "lawngreen",
            "chartreuse",
            "aquamarine",
            "maroon",
            "purple",

            "olive",
            "grey",
            "skyblue",
            "lightskyblue",
            "blueviolet",

            "darkred",
            "darkmagenta",
            "saddlebrown",
            "darkseagreen",
            "lightgreen",

            "mediumpurple",
            "darkviolet",
            "palegreen",
            "darkorchid",
            "yellowgreen",

            "sienna",
            "brown",
            "darkgrey",
            "lightblue",
            "greenyellow",

            "paleturquoise",
            "lightsteelblue",
            "powderblue",
            "firebrick",
            "darkgoldenrod",

            "mediumorchid",
            "rosybrown",
            "darkkhaki",
            "silver",
            "mediumvioletred",

            "indianred",
            "peru",
            "chocolate",
            "tan",
            "lightgrey",

            "thistle",
            "orchid",
            "goldenrod",
            "palevioletred",
            "crimson",

            "gainsboro",
            "plum",
            "burlywood",
            "lightcyan",
            "lavender",

            "darksalmon",
            "violet",
            "palegoldenrod",
            "lightcoral",
            "khaki",

            "aliceblue",
            "honeydew",
            "azure",
            "sandybrown",
            "wheat",

            "beige",
            "whitesmoke",
            "mintcream",
            "ghostwhite",
            "salmon",

            "antiquewhite",
            "linen",
            "lightgoldenrodyellow",
            "oldlace",
            "red",

            "magenta",
            "deeppink",
            "orangered",
            "tomato",
            "hotpink",

            "coral",
            "darkorange",
            "lightsalmon",
            "orange",
            "lightpink",

            "pink",
            "gold",
            "peachpuff",
            "navajowhite",
            "moccasin",

            "bisque",
            "mistyrose",
            "blanchedalmond",
            "papayawhip",
            "lavenderblush",

            "seashell",
            "cornsilk",
            "lemonchiffon",
            "floralwhite",
            "snow",

            "yellow",

            "lightyellow",
            "ivory",
            "white",

            "black",
            "black",
            "black",

            "snow",
            "white",
            "white",

            "red",
            "red",
            "maroon",

            "lime",
            "limegreen",
            "green",

            "blue",
            "blue",
            "mediumblue"
        ]

        for rgb, name in zip(rgb_values, expected_names):
            self.assertEqual(utilities.rgb_to_the_closest_color_name(rgb), name)

    def test_read_palette_from_file(self):
        palette = utilities.read_palette_from_file("test_palette2.txt")
        expected_palette = (255, 255, 255, 0, 0, 0, 255, 0, 0, 7, 164, 65, 14, 2, 176, 255, 86, 193)
        self.assertEqual(palette, expected_palette)

    def test_save_palette_to_file(self):
        expected_palette = (255, 255, 255, 0, 0, 0, 255, 0, 0, 7, 164, 65, 14, 2, 176, 255, 86, 193)
        utilities.save_palette_to_file("test_palette2.txt", expected_palette)
        palette = utilities.read_palette_from_file("test_palette2.txt")
        self.assertEqual(palette, expected_palette)

    def test_generate_palette_color_names(self):
        palette = (255, 255, 255, 0, 0, 0, 255, 0, 0, 7, 164, 65, 14, 2, 176, 255, 86, 193)
        palette_color_names = utilities.generate_palette_color_names(palette)
        expected_color_names = ["white", "black", "red", "forestgreen", "mediumblue", "hotpink"]
        self.assertEqual(palette_color_names, expected_color_names)
