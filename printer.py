from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, Motor
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
import time
from ev3dev2.sound import Sound
import utilities


class Printer:
    colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

    def __init__(self, pixel_size):
        self._touch = TouchSensor(INPUT_1)
        self._color = ColorSensor(INPUT_2)
        self._color.mode = 'COL-COLOR'
        self._fb_motor = LargeMotor(OUTPUT_C)
        self._lr_motor = LargeMotor(OUTPUT_B)
        self._ud_motor = Motor(OUTPUT_A)

        self._x_res = utilities.MAX_X_RES / int(pixel_size)
        self._y_res = utilities.MAX_Y_RES / int(pixel_size)
        self.padding_left = utilities.MAX_PADDING_LEFT / int(pixel_size)
        self.padding_right = utilities.MAX_PADDING_RIGHT / int(pixel_size)
        self._is_pen_up = True
        self._pen_calibrated = False

        self._ud_ratio = 5
        self._fb_ratio = 5
        self._lr_ratio = 1
        self._pen_up_val = -3 * self._ud_ratio
        self._pen_down_val = -self._pen_up_val
        self._pen_up_down_speed = 10
        self._pen_left_speed = 15
        self._pen_right_speed = 10
        self._paper_scroll_speed = 20

        self._pixel_size = pixel_size
        self._p_codes = []
        self._current_line = 0

    def _pen_up(self, val):
        print("{} {}".format('PEN_UP', val))
        self._ud_motor.on_for_degrees(self._pen_up_down_speed, val * self._pen_up_val)
        self._is_pen_up = True

    def _pen_down(self, val):
        print("{} {}".format('PEN_DOWN', val))
        self._ud_motor.on_for_degrees(self._pen_up_down_speed, val * self._pen_down_val)
        self._is_pen_up = False

    def _pen_left(self, val):
        print("{} {}".format('PEN_LEFT', val))
        self._lr_motor.on_for_degrees(self._pen_left_speed, int(self._pixel_size) * val * self._lr_ratio)

    def _pen_right(self, val):
        print("{} {}".format('PEN_RIGHT', val))
        self._lr_motor.on_for_degrees(self._pen_right_speed, -int(self._pixel_size) * val * self._lr_ratio)

    def _paper_scroll(self, val):
        print("{} {}".format('SCROLL', val))
        self._current_line += 1
        print("-------------- Line {} --------------".format(self._current_line))
        self._fb_motor.on_for_degrees(self._paper_scroll_speed, int(self._pixel_size) * val * self._fb_ratio)

    def _finish_calibration(self):
        self._pen_calibrated = True

    def calibrate(self):
        speaker = Sound()
        speaker.speak("Calibrating")
        btn = Button()

        self._lr_motor.reset()
        self._ud_motor.reset()
        self._fb_motor.reset()

        self._lr_motor.on_for_degrees(10, 320)
        self._lr_motor.reset()

        self._ud_motor.on(-15)
        self._touch.wait_for_pressed()
        self._ud_motor.stop()
        time.sleep(1)
        self._ud_motor.on(15)
        self._touch.wait_for_released()
        self._ud_motor.on_for_degrees(10, 40)
        self._ud_motor.stop()
        time.sleep(1)

        speaker.speak("Insert calibration paper and press the touch sensor")
        self._touch.wait_for_pressed()
        speaker.speak("Adjust pen height")

        while not self._pen_calibrated:
            self._lr_motor.on_for_degrees(10, -100)
            self._lr_motor.on_for_degrees(10, 100)
            time.sleep(1)
            if btn.up:
                self._pen_up(1)
            elif btn.down:
                self._pen_down(1)
            elif btn.right:
                self._finish_calibration()
            elif btn.left:
                self._pen_down(4)

        self._lr_motor.reset()
        self._pen_up(1)
        speaker.speak("Insert a blank piece of paper and press the touch sensor")
        self._touch.wait_for_pressed()

        self._lr_motor.stop()
        self._lr_motor.on_for_degrees(10, 120)
        self._lr_motor.reset()

        self._fb_motor.on(5)
        val = 0
        while self.colors[val] == 'unknown':
            val = self._color.value()
            print("Color = {}".format(self.colors[val]))

        self._fb_motor.reset()

    def draw(self, path=None):
        speaker = Sound()

        if path is not None:
            binarized, img_x, img_y = utilities.binarize_image(path, self._x_res, self._y_res)
            speaker.speak("Printing image")
            print("\nPrinting image...")
        else:
            binarized, img_x, img_y = utilities.generate_and_binarize_test_image(self._pixel_size)
            speaker.speak("Printing test page")
            print("\nPrinting test page...")

        p_codes = utilities.binarized_image_to_p_codes(binarized, img_x, img_y)
        btn = Button()

        print("---------- p_codes:----------")
        print("-------------- Line {} --------------".format(self._current_line))
        for x in p_codes:
            if btn.down:
                speaker.speak("Aborting")
                print("\nAborting...")
                break

            if x[0] == utilities.Command.PEN_UP:
                if not self._is_pen_up:
                    self._pen_up(x[1])

            elif x[0] == utilities.Command.PEN_DOWN:
                if self._is_pen_up:
                    self._pen_down(x[1])

            elif x[0] == utilities.Command.PEN_RIGHT:
                self._pen_right(x[1])

            elif x[0] == utilities.Command.PEN_LEFT:
                self._pen_left(x[1])

            elif x[0] == utilities.Command.SCROLL:
                self._paper_scroll(x[1])

        self._ud_motor.on_for_degrees(self._pen_up_down_speed, self._pen_up_val)
        self._ud_motor.stop()
        # self._fb_motor.on_for_degrees(10, 360)
        self._paper_scroll(self._y_res)
        self._fb_motor.reset()
        self._ud_motor.reset()
        self._lr_motor.reset()

        speaker = Sound()
        speaker.speak("Printing finished")
        print("Printing finished")
