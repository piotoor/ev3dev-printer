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
