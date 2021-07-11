#!/usr/bin/env python3
import printer


if __name__ == '__main__':
    ptr = printer.Printer(2)
    ptr.calibrate()

    ptr.draw(path="skorpjen.png")
    # ptr.draw()
