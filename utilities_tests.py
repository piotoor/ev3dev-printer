import unittest
import utilities


class BinarizedImageToPCodesTests(unittest.TestCase):
    def test_single_pixel(self):
        x_res = 1
        y_res = 1

        binarized = [True]
        p_codes = utilities.binarized_image_to_p_codes(binarized, x_res, y_res)
        expected_p_codes = [
            [utilities.Command.PEN_DOWN, 0],
            [utilities.Command.PEN_RIGHT, 0],
            [utilities.Command.PEN_UP, 0],
            [utilities.Command.PEN_LEFT, x_res - 1],
            [utilities.Command.SCROLL, 1]
        ]
        self.assertEqual(p_codes, expected_p_codes)

        binarized = [False]
        p_codes = utilities.binarized_image_to_p_codes(binarized, x_res, y_res)
        expected_p_codes = [
            [utilities.Command.PEN_RIGHT, 0],
            [utilities.Command.PEN_LEFT, x_res - 1],
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

        expected_p_codes = [
            [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1]
            ],

            [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1]
            ],

            [
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1]
            ],

            [
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1]
            ]
        ]

        for images, expected in zip(binarized_testcases, expected_p_codes):
            p_codes = utilities.binarized_image_to_p_codes(images, x_res, y_res)
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

        expected_p_codes = [
            [
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],
            # ------------------------------------------------------------
            [
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],
            # ------------------------------------------------------------
            [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],
            # ------------------------------------------------------------
            [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 0],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ],

            [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],

                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, 1],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
            ]
        ]

        for images, expected in zip(binarized_testcases, expected_p_codes):
            p_codes = utilities.binarized_image_to_p_codes(images, x_res, y_res)
            self.assertEqual(p_codes, expected)

    def test_10x10_alternating_rows(self):
        x_res = 10
        y_res = 10

        binarized = [
            (x // 10) % 2 == 0 for x in range(x_res * y_res)
        ]

        expected_p_codes = [
                [utilities.Command.PEN_DOWN, 0],
                [utilities.Command.PEN_RIGHT, x_res - 1],
                [utilities.Command.PEN_UP, 0],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1],
                [utilities.Command.PEN_RIGHT, x_res - 1],
                [utilities.Command.PEN_LEFT, x_res - 1],
                [utilities.Command.SCROLL, 1]
        ] * (x_res // 2)

        p_codes = utilities.binarized_image_to_p_codes(binarized, x_res, y_res)
        self.assertEqual(p_codes, expected_p_codes)
