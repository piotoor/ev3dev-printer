import unittest
import utilities
from parameterized import parameterized_class, parameterized


class BinarizedImageToPCodesTests(unittest.TestCase):
    def test_single_pixel(self):
        x_res = 1
        y_res = 1

        for pixel_size in [1, 2, 4]:
            padding_left = utilities.MAX_PADDING_LEFT / pixel_size
            binarized = [True]
            p_codes = utilities.binarized_image_to_p_codes(binarized, x_res, y_res, padding_left)
            expected_p_codes = [
                [utilities.Command.PEN_RIGHT, padding_left],
                [utilities.Command.PEN_DOWN, 1],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 1],
                [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                [utilities.Command.PEN_RIGHT, padding_left],
                [utilities.Command.SCROLL, 1]
            ]
            self.assertEqual(p_codes, expected_p_codes)

            binarized = [False]
            p_codes = utilities.binarized_image_to_p_codes(binarized, x_res, y_res, padding_left)
            expected_p_codes = [
                [utilities.Command.PEN_RIGHT, padding_left],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                [utilities.Command.PEN_RIGHT, padding_left],
                [utilities.Command.SCROLL, 1]
                ]
            self.assertEqual(p_codes, expected_p_codes)

    def test_2x1(self):
        x_res = 2
        y_res = 1

        binarized_testcases = [
            [True, True],
            [True, False],
            [False, True],
            [False, False]
        ]

        for pixel_size in [1, 2, 4]:
            padding_left = utilities.MAX_PADDING_LEFT / pixel_size
            expected_p_codes = [
                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1]
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1]
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1]
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1]
                ]
            ]

            for images, expected in zip(binarized_testcases, expected_p_codes):
                p_codes = utilities.binarized_image_to_p_codes(images, x_res, y_res, padding_left)
                self.assertEqual(p_codes, expected)

    def test_2x2(self):
        x_res = 2
        y_res = 2

        binarized_testcases = [
            [False, False,
             False, False],

            [False, False,
             False, True],

            [False, False,
             True, False],

            [False, False,
             True, True],
            # --------------------------------
            [False, True,
             False, False],

            [False, True,
             False, True],

            [False, True,
             True, False],

            [False, True,
             True, True],
            # --------------------------------
            [True, False,
             False, False],

            [True, False,
             False, True],

            [True, False,
             True, False],

            [True, False,
             True, True],
            # --------------------------------
            [True, True,
             False, False],

            [True, True,
             False, True],

            [True, True,
             True, False],

            [True, True,
             True, True]
        ]

        for pixel_size in [1, 2, 4]:
            padding_left = utilities.MAX_PADDING_LEFT / pixel_size
            expected_p_codes = [
                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],
                # ------------------------------------------------------------
                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],
                # ------------------------------------------------------------
                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],
                # ------------------------------------------------------------
                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 0],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ],

                [
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],

                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, 1],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                ]
            ]

            for images, expected in zip(binarized_testcases, expected_p_codes):
                p_codes = utilities.binarized_image_to_p_codes(images, x_res, y_res, padding_left)
                self.assertEqual(p_codes, expected)

    def test_10x10_alternating_rows(self):
        x_res = 10
        y_res = 10

        binarized = [
            (x // 10) % 2 == 0 for x in range(x_res * y_res)
        ]

        for pixel_size in [1, 2, 4]:
            padding_left = utilities.MAX_PADDING_LEFT / pixel_size
            expected_p_codes = [
                    [utilities.Command.PEN_DOWN, 1],
                    [utilities.Command.PEN_RIGHT, x_res - 1],
                    [utilities.Command.PEN_UP, 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
                    [utilities.Command.PEN_RIGHT, x_res - 1],
                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1]
            ] * (x_res // 2)

            expected_p_codes = [[utilities.Command.PEN_RIGHT, padding_left]] + expected_p_codes
            p_codes = utilities.binarized_image_to_p_codes(binarized, x_res, y_res, padding_left)
            self.assertEqual(p_codes, expected_p_codes)

    def test_10x10_alternating_cols(self):
        x_res = 10
        y_res = 10

        binarized = [
            x % 2 == 0 for x in range(x_res * y_res)  # works only for even x_res
        ]

        for pixel_size in [1, 2, 4]:
            padding_left = utilities.MAX_PADDING_LEFT / pixel_size
            expected_p_codes = [
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

                    [utilities.Command.PEN_LEFT, x_res - 1 + padding_left],
                    [utilities.Command.PEN_RIGHT, padding_left],
                    [utilities.Command.SCROLL, 1],
            ] * y_res

            expected_p_codes = [[utilities.Command.PEN_RIGHT, padding_left]] + expected_p_codes
            p_codes = utilities.binarized_image_to_p_codes(binarized, x_res, y_res, padding_left)
            self.assertEqual(p_codes, expected_p_codes)


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
    def test_generate_and_binarize_calibration_test_image(self, _, pixel_size, expected ):
        binarized, img_x, img_y = utilities.generate_and_binarize_calibration_test_image(pixel_size)
        expected_x_res, expected_y_res = expected
        self.assertEqual(expected_x_res * expected_y_res, len(binarized[0]))
