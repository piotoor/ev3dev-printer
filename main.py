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
        SCROLL = 4

    colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

    def __init__(self, pixel_size):
        self.touch = TouchSensor(INPUT_1)
        self.color = ColorSensor(INPUT_2)
        self.color.mode = 'COL-COLOR'
        self.fb_motor = LargeMotor(OUTPUT_C)
        self.lr_motor = LargeMotor(OUTPUT_B)
        self.ud_motor = Motor(OUTPUT_A)

        self.x_res = 320 / pixel_size
        self.y_res = 360 / pixel_size
        self.is_pen_up = True
        self.pen_calibrated = False

        self.ud_ratio = 5
        self.fb_ratio = 5
        self.lr_ratio = 1
        self.pen_up_val = -3 * self.ud_ratio
        self.pen_down_val = -self.pen_up_val
        self.pen_up_down_speed = 10
        self.pen_left_speed = 20
        self.pen_right_speed = 10
        self.paper_scroll_speed = 10

        self.pixel_size = pixel_size
        self.p_codes = []
        self.binarized = []

    def read_image_from_file(self, path):
        img = Image.open(path).convert('1').resize((self.x_res, self.y_res))
        pixels = list(img.getdata())
        self.binarized = list(map(lambda val: not val, pixels))

    def generate_test_image(self):
        no_of_alternating_horizontal_strips = int(self.y_res // 4)
        no_of_chessboard_rows = int(self.y_res // 2)
        cols = int(self.x_res)

        for i in range(0, no_of_chessboard_rows):
            white_square = i % 2 == 0
            for col in range(0, cols):
                self.binarized.append(white_square)
                white_square = not white_square

        for i in range(0, no_of_alternating_horizontal_strips):
            for col in range(0, cols):
                self.binarized.append(True)
            for col in range(0, cols):
                self.binarized.append(False)

    def image_to_p_codes(self):
        rows = int(self.y_res)
        cols = int(self.x_res)

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
            self.p_codes.append([self.Command.SCROLL, 1])

    def pen_up(self, val):
        print("{} {}".format('PEN_UP', val))
        self.ud_motor.on_for_degrees(self.pen_up_down_speed, val)
        self.is_pen_up = True

    def pen_down(self, val):
        print("{} {}".format('PEN_DOWN', val))
        self.ud_motor.on_for_degrees(self.pen_up_down_speed, val)
        self.is_pen_up = False

    def pen_left(self, val):
        print("{} {}".format('LEFT', val))
        self.lr_motor.on_for_degrees(self.pen_left_speed, self.pixel_size * val * self.lr_ratio)

    def pen_right(self, val):
        print("{} {}".format('RIGHT', val))
        self.lr_motor.on_for_degrees(self.pen_right_speed, -self.pixel_size * val * self.lr_ratio)

    def paper_scroll(self, val):
        print("{} {}".format('SCROLL', val))
        self.fb_motor.on_for_degrees(self.paper_scroll_speed, self.pixel_size * val * self.fb_ratio)

    def finish_calibration(self):
        self.pen_calibrated = True

    def calibrate(self):
        speaker = Sound()
        speaker.speak("Calibrating")
        btn = Button()

        self.lr_motor.reset()
        self.ud_motor.reset()
        self.fb_motor.reset()

        self.lr_motor.on_for_degrees(10, 320)
        self.lr_motor.reset()

        self.ud_motor.on(-15)
        self.touch.wait_for_pressed()
        self.ud_motor.stop()
        time.sleep(1)
        self.ud_motor.on(15)
        self.touch.wait_for_released()
        self.ud_motor.on_for_degrees(10, 40)
        self.ud_motor.stop()
        time.sleep(1)

        speaker.speak("Insert calibration paper and press the touch sensor")
        self.touch.wait_for_pressed()
        speaker.speak("Adjust pen height")

        while not self.pen_calibrated:
            self.lr_motor.on_for_degrees(10, -100)
            self.lr_motor.on_for_degrees(10, 100)
            time.sleep(1)
            if btn.up:
                self.pen_up(self.pen_up_val)
            elif btn.down:
                self.pen_down(self.pen_down_val * 2)
            elif btn.right:
                self.finish_calibration()
            elif btn.left:
                self.pen_down(self.ud_ratio)

        self.lr_motor.reset()
        self.pen_up(self.pen_up_val)
        speaker.speak("Insert a blank piece of paper and press the touch sensor")
        self.touch.wait_for_pressed()

        self.lr_motor.stop()
        self.lr_motor.on_for_degrees(10, 120)
        self.lr_motor.reset()

        self.fb_motor.on(5)
        val = 0
        while self.colors[val] == 'unknown':
            val = self.color.value()
            print("Color = {}".format(self.colors[val]))

        self.fb_motor.reset()

    def draw(self, path=None):
        speaker = Sound()
        if path is not None:
            self.read_image_from_file(path)
            speaker.speak("Printing")
        else:
            self.generate_test_image()
            speaker.speak("Printing test page")

        self.image_to_p_codes()

        print("p_codes:\n")
        line = 0
        for x in self.p_codes:
            print("------- Line number: {} / {} -------".format(line, self.y_res))
            line += 1

            if x[0] == self.Command.PEN_UP:
                if not self.is_pen_up:
                    self.pen_up(self.pen_up_val)

            elif x[0] == self.Command.PEN_DOWN:
                if self.is_pen_up:
                    self.pen_down(self.pen_down_val)

            elif x[0] == self.Command.RIGHT:
                self.pen_right(x[1])

            elif x[0] == self.Command.LEFT:
                self.pen_left(x[1])

            elif x[0] == self.Command.SCROLL:
                self.paper_scroll(x[1])

            print("lr_motor.pos: {}".format(self.lr_motor.position))

        self.ud_motor.on_for_degrees(10, self.pen_up_val)
        self.ud_motor.stop()
        self.fb_motor.on_for_degrees(10, -360)
        self.fb_motor.stop()
        self.fb_motor.reset()

        speaker = Sound()
        speaker.speak("Printing finished")


if __name__ == '__main__':
    printer = Printer(2)
    printer.calibrate()

    # printer.draw("skorpjen.png")
    printer.draw()
