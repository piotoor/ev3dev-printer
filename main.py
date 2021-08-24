#!/usr/bin/env python3
import printer
import utilities
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pixel_size", type=int, choices={1, 2, 4}, default=2)
    parser.add_argument("-f", "--file_name")
    # parser.add_argument("-q", "--quick_calibration", action="store_true")
    parser.add_argument("-m", "--multi_color", action="store_true")
    parser.add_argument("-c", "--calibrate_palette", action="store_true")
    args = parser.parse_args()

    if args.pixel_size == 1:
        ptr = printer.Printer(utilities.PixelSize.PIXEL_1x1)
    elif args.pixel_size == 2:
        ptr = printer.Printer(utilities.PixelSize.PIXEL_2x2)
    else:
        ptr = printer.Printer(utilities.PixelSize.PIXEL_4x4)

    # ptr.calibrate(args.quick_calibration)
    if args.file_name:
        ptr.draw(args.file_name, args.multi_color, args.calibrate_palette)
    else:
        ptr.draw()
