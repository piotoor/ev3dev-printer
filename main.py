#!/usr/bin/env python3
import printer
import utilities

if __name__ == '__main__':
    ptr = printer.Printer(utilities.PixelSize.PIXEL_2x2)
    ptr.calibrate()

    ptr.draw(path="skorpjen.png")
    # ptr.draw()
