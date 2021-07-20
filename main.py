#!/usr/bin/env python3
import printer
import utilities
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pixel_size", type=int, choices={1, 2, 4}, default=2)
    parser.add_argument("-f", "--file_name")
    args = parser.parse_args()

    if args.pixel_size == 1:
        ptr = printer.Printer(utilities.PixelSize.PIXEL_1x1)
    elif args.pixel_size == 2:
        ptr = printer.Printer(utilities.PixelSize.PIXEL_2x2)
    else:
        ptr = printer.Printer(utilities.PixelSize.PIXEL_4x4)

    ptr.calibrate()
    if args.file_name:
        ptr.draw(args.file_name)
    else:
        ptr.draw()
