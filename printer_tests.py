import unittest
import printer


class BinarizedImageToPCodesTests(unittest.TestCase):
    def test_single_pixel(self):
        x_res = 1
        y_res = 1

        binarized = [True]
        p_codes = printer.binarized_image_to_p_codes(binarized, x_res, y_res)
        expected_p_codes = [
            [printer.Command.PEN_DOWN, 0],
            [printer.Command.PEN_RIGHT, 0],
            [printer.Command.PEN_UP, 0],
            [printer.Command.PEN_LEFT, x_res - 1],
            [printer.Command.SCROLL, 1]
        ]
        self.assertEqual(p_codes, expected_p_codes)

        binarized = [False]
        p_codes = printer.binarized_image_to_p_codes(binarized, x_res, y_res)
        expected_p_codes = [
            [printer.Command.PEN_RIGHT, 0],
            [printer.Command.PEN_LEFT, x_res - 1],
            [printer.Command.SCROLL, 1]
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
                [printer.Command.PEN_DOWN, 0],
                [printer.Command.PEN_RIGHT, 1],
                [printer.Command.PEN_UP, 0],
                [printer.Command.PEN_LEFT, x_res - 1],
                [printer.Command.SCROLL, 1]
            ],

            [
                [printer.Command.PEN_DOWN, 0],
                [printer.Command.PEN_RIGHT, 0],
                [printer.Command.PEN_UP, 0],
                [printer.Command.PEN_RIGHT, 1],
                [printer.Command.PEN_LEFT, x_res - 1],
                [printer.Command.SCROLL, 1]
            ],

            [
                [printer.Command.PEN_RIGHT, 1],
                [printer.Command.PEN_DOWN, 0],
                [printer.Command.PEN_RIGHT, 0],
                [printer.Command.PEN_UP, 0],
                [printer.Command.PEN_LEFT, x_res - 1],
                [printer.Command.SCROLL, 1]
            ],

            [
                [printer.Command.PEN_RIGHT, 1],
                [printer.Command.PEN_LEFT, x_res - 1],
                [printer.Command.SCROLL, 1]
            ]
        ]

        for images, expected in zip(binarized_testcases, expected_p_codes):
            p_codes = printer.binarized_image_to_p_codes(images, x_res, y_res)
            self.assertEqual(p_codes, expected)