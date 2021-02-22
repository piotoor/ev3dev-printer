#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, Motor
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
from PIL import Image
from enum import Enum
import time
from ev3dev2.sound import Sound


class Printer:
    class Command(Enum):
        PEN_UP = 0
        PEN_DOWN = 1
        RIGHT = 2
        LEFT = 3
        DOWN = 4

    colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

    def __init__(self, pixel_size):
        self.touch = TouchSensor(INPUT_1)
        self.color = ColorSensor(INPUT_2)
        self.color.mode = 'COL-COLOR'
        self.fb_motor = LargeMotor(OUTPUT_B)
        self.lr_motor = LargeMotor(OUTPUT_C)
        self.ud_motor = Motor(OUTPUT_A)

        self.x_res = 320 / pixel_size
        self.y_res = 360 / pixel_size
        self.pen_up = True
        self.pen_calibrated = False
        self.pen_up_val = 3
        self.pixel_size = pixel_size
        self.p_codes = []
        self.binarized = []

    def read_image_from_file(self, path):
        img = Image.open(path).convert('1').resize((self.x_res, self.y_res))
        pixels = list(img.getdata())
        self.binarized = list(map(lambda val: not val, pixels))

    def generate_test_image(self):
        rows = self.y_res
        cols = self.x_res

    def image_to_p_codes(self, path):
        rows = self.y_res
        cols = self.x_res


        # print(self.binarized)

        for i in range(rows):
            prev = self.binarized[i * cols]

            if prev:
                self.p_codes.append([self.Command.PEN_DOWN, 0])
            self.p_codes.append([self.Command.RIGHT, 0])

            for j in range(1, cols):
                curr = self.binarized[i * cols + j]
                if curr == prev:
                    self.p_codes[-1][1] += 1
                else:
                    if curr:
                        self.p_codes.append([self.Command.PEN_DOWN, 0])
                        self.p_codes.append([self.Command.RIGHT, 0])
                    else:
                        self.p_codes.append([self.Command.PEN_UP, 0])
                        self.p_codes.append([self.Command.RIGHT, 2])

                prev = curr

            self.p_codes.append([self.Command.PEN_UP, 0])
            self.p_codes.append([self.Command.LEFT, self.x_res])
            self.p_codes.append([self.Command.DOWN, 1])

    def up(self):
        self.ud_motor.on_for_degrees(10, self.pen_up_val)

    def down(self, x):
        self.ud_motor.on_for_degrees(10, -x)

    def ok(self):
        self.pen_calibrated = True

    def calibrate(self):
        spkr = Sound()
        spkr.speak("Calibrating")
        btn = Button()

        self.lr_motor.stop()
        self.lr_motor.on_for_degrees(10, 320)
        self.lr_motor.reset()

        self.ud_motor.on(15)
        self.touch.wait_for_pressed()
        self.ud_motor.stop()
        time.sleep(1)
        self.ud_motor.on(-15)
        self.touch.wait_for_released()
        self.ud_motor.on_for_degrees(10, -20)
        self.ud_motor.stop()
        time.sleep(1)

        spkr.speak("Insert calibration paper and press the touch sensor")
        self.touch.wait_for_pressed()
        spkr.speak("Adjust pen height")

        while not self.pen_calibrated:
            self.lr_motor.on_for_degrees(10, -100)
            self.lr_motor.on_for_degrees(10, 100)
            time.sleep(1)
            if btn.up:
                self.up()
            elif btn.down:
                self.down(self.pen_up_val)
            elif btn.right:
                self.ok()
            elif btn.left:
                self.down(1)

        self.lr_motor.reset()
        self.ud_motor.on_for_degrees(10, self.pen_up_val)
        spkr.speak("Insert a blank piece of paper and press the touch sensor")
        self.touch.wait_for_pressed()

        self.lr_motor.stop()
        self.lr_motor.on_for_degrees(10, 120)
        self.lr_motor.reset()

        self.fb_motor.on(-5)
        val = 0
        while self.colors[val] == 'unknown':
            val = self.color.value()
            print("Color = {}".format(self.colors[val]))

        self.fb_motor.reset()

    def draw(self, path=None):
        spkr = Sound()
        if path is not None:
            self.read_image_from_file(path)
            spkr.speak("Printing")
        else:
            self.generate_test_image()
            spkr.speak("Printing test page")

        self.image_to_p_codes()

        print("p_codes:\n")
        line = 0
        for x in self.p_codes:
            print("------- Line number: {} / {} -------".format(line, self.y_res))
            line += 1

            if x[0] == self.Command.PEN_UP:
                if not self.pen_up:
                    print("{} {}".format('PEN_UP', x[1]))
                    self.ud_motor.on_for_degrees(15, self.pen_up_val)
                    self.pen_up = True
            elif x[0] == self.Command.PEN_DOWN:
                if self.pen_up:
                    print("{} {}".format('PEN_DOWN', x[1]))
                    self.ud_motor.on_for_degrees(15, -self.pen_up_val)
                    self.pen_up = False
            elif x[0] == self.Command.RIGHT:
                print("{} {}".format('RIGHT', x[1]))
                self.lr_motor.on_for_degrees(10, -self.pixel_size * x[1])
            elif x[0] == self.Command.LEFT:
                print("{} {}".format('LEFT', x[1]))
                self.lr_motor.on_for_degrees(20, self.pixel_size * x[1])
            elif x[0] == self.Command.DOWN:
                print("{} {}".format('DOWN', x[1]))
                self.fb_motor.on_for_degrees(10, -self.pixel_size * x[1])

            print("lr_motor.pos: {}".format(self.lr_motor.position))

        self.ud_motor.on_for_degrees(10, self.pen_up_val)
        self.ud_motor.stop()
        self.fb_motor.on_for_degrees(10, -360)
        self.fb_motor.stop()
        self.fb_motor.reset()

        spkr = Sound()
        spkr.speak("Printing finished")


if __name__ == '__main__':
    # printer = Printer(160, 180)
    printer = Printer(1)
    printer.calibrate()

    printer.draw("skorpjen.png")
    # printer.draw()
