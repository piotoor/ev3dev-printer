from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, Motor
from ev3dev2.sensor import INPUT_1, INPUT_4
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
        self._color = ColorSensor(INPUT_4)
        self._color.mode = 'COL-COLOR'
        self._fb_motor = LargeMotor(OUTPUT_C)
        self._lr_motor = LargeMotor(OUTPUT_B)
        self._ud_motor = Motor(OUTPUT_A)

        self._x_res = utilities.MAX_X_RES / int(pixel_size)
        self._y_res = utilities.MAX_Y_RES / int(pixel_size)
        self._padding_left = utilities.MAX_PADDING_LEFT / int(pixel_size)
        self._padding_right = utilities.MAX_PADDING_RIGHT / int(pixel_size)
        self._is_pen_up = True
        self._pen_calibrated = False

        self._ud_ratio = 5
        self._fb_ratio = 4
        self._lr_ratio = 1
        self._pen_up_val = -3 * self._ud_ratio
        self._pen_down_val = -self._pen_up_val
        self._pen_up_down_speed = 10
        self._pen_left_speed = 20
        self._pen_right_speed = 20
        self._paper_scroll_speed = 20

        self._palette = []
        self._palette_color_names = ["black"]
        self._num_of_colors = 2
        self._pixel_size = pixel_size
        self._p_codes = []
        self._current_line = 0

    def _pen_up(self, val):
        print("{} {}".format('PEN_UP', val))
        if val > 0:
            self._ud_motor.on_for_degrees(self._pen_up_down_speed, val * self._pen_up_val)
            self._is_pen_up = True

    def _pen_down(self, val):
        print("{} {}".format('PEN_DOWN', val))
        if val > 0:
            self._ud_motor.on_for_degrees(self._pen_up_down_speed, val * self._pen_down_val)
            self._is_pen_up = False

    def _pen_left(self, val):
        print("{} {}".format('PEN_LEFT', val))
        if val > 0:
            self._lr_motor.on_for_degrees(self._pen_left_speed, int(self._pixel_size) * val * self._lr_ratio)

    def _pen_right(self, val):
        print("{} {}".format('PEN_RIGHT', val))
        if val > 0:
            self._lr_motor.on_for_degrees(self._pen_right_speed, -int(self._pixel_size) * val * self._lr_ratio)

    def _paper_scroll(self, val):
        print("{} {}".format('SCROLL', val))
        if val > 0:
            if val == 1:
                self._current_line += val
                print("-------------- Line {} --------------".format(self._current_line))
            self._fb_motor.on_for_degrees(self._paper_scroll_speed, int(self._pixel_size) * val * self._fb_ratio)

    def _finish_calibration(self):
        self._pen_calibrated = True

    def _palette_calibration(self):
        curr_color_mode = self._color.mode
        self._color.mode = 'RGB-RAW'

        calibration_done = False

        speaker = Sound()
        palette = []
        self._fb_motor.reset()
        self._fb_motor.on(5)
        initial_vals = prev_vals = self._color.rgb
        epsilon = 10
        new_color = True

        while not calibration_done and not self._touch.value():
            vals = self._color.rgb
            delta_prev_vals = (abs(vals[0] - prev_vals[0]), abs(vals[1] - prev_vals[1]), abs(vals[2] - prev_vals[2]))
            delta_init_vals = (
                abs(vals[0] - initial_vals[0]), abs(vals[1] - initial_vals[1]), abs(vals[2] - initial_vals[2]))

            if len(palette) > 0:
                delta_last_vals = (
                    abs(vals[0] - palette[-1][0]), abs(vals[1] - palette[-1][1]), abs(vals[2] - palette[-1][2]))
            else:
                delta_last_vals = (3 * epsilon, 3 * epsilon, 3 * epsilon)

            if (len(palette) > 1 and max(delta_init_vals) <= 2 * epsilon and new_color) or abs(
                    self._fb_motor.position) > 360 * self._fb_ratio:
                calibration_done = True
                new_color = False
            elif max(delta_prev_vals) <= epsilon and new_color and max(delta_last_vals) >= 2 * epsilon:
                palette.append(vals)
                print("Added {} to palette".format(vals))
                new_color = False

            else:
                new_color = True

            prev_vals = vals
            time.sleep(0.5)

        if len(palette) < 2:
            print("Invalid palette")
        else:
            print("Palette has been generated. Available colors:")
            speaker.speak("Palette has been generated. Available colors:")
            for x in palette:
                print(utilities.rgb_to_the_closest_color_name(x))
                speaker.speak("{}".format(utilities.rgb_to_the_closest_color_name(x)))

        for x in palette:
            for y in x:
                self._palette.append(y)

        self._color.mode = curr_color_mode
        self._fb_motor.reset()
        utilities.save_palette_to_file("palette.txt", self._palette)

    def _pen_calibration(self, quick_calibration):
        speaker = Sound()

        if quick_calibration:
            speaker.speak("Quick calibration")
            print("Quick calibration...")
        else:
            speaker.speak("Calibrating")
            print("Calibrating...")
            btn = Button()

            self._lr_motor.reset()
            self._ud_motor.reset()
            self._fb_motor.reset()

            self._lr_motor.on_for_degrees(self._pen_left_speed, self._x_res * self._pixel_size * self._lr_ratio)
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
            print("Adjust pen height...")

            while not self._pen_calibrated:
                self._lr_motor.on_for_degrees(self._pen_right_speed, -100 * self._pixel_size * self._lr_ratio)
                self._lr_motor.on_for_degrees(self._pen_left_speed, 100 * self._pixel_size * self._lr_ratio)
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

        if not self._is_pen_up:
            self._pen_up(1)
        self._pen_left(self._x_res)

        for _ in range(2):
            self._pen_right(self._x_res)
            self._pen_left(self._x_res)
        for _ in range(8):
            self._pen_right(self._padding_left)
            for _ in range(int(self._x_res)):
                self._pen_right(1)
            self._pen_left(self._x_res + self._padding_left)
        self._lr_motor.reset()

        speaker.speak("Insert a blank piece of paper and press the touch sensor")
        self._touch.wait_for_pressed()
        self._fb_motor.on(5)
        val = 0
        print("Scrolling the piece of paper to its starting position...")
        while self.colors[val] == 'black':
            val = self._color.value()

        self._fb_motor.reset()
        print("Calibration done")

    def _interpret_p_codes(self, p_codes):
        btn = Button()
        speaker = Sound()
        self._current_line = 0
        abort = False

        print("---------- p_codes:----------")
        print("-------------- Line {} --------------".format(self._current_line))
        for x in p_codes:
            if btn.down:
                speaker.speak("Aborting")
                print("\nAborting...")
                abort = True
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

        if not self._is_pen_up:
            self._pen_up(1)
        self._ud_motor.stop()

        return abort

    def draw(self, path=None, multicolor=False, force_palette_calibration=False):
        speaker = Sound()

        if path is not None:
            if multicolor:
                speaker.speak("Printing multi color image")
                print("\nPrinting multi color image...")

                if force_palette_calibration:
                    print("Forced palette calibration")
                    speaker.speak("Forced palette calibration")
                    self._palette_calibration()
                else:
                    try:
                        self._palette = utilities.read_palette_from_file("palette.txt")
                        # validate size of palette
                    except IOError:
                        print("Error reading palette from file. Palette calibration needed")
                        speaker.speak("Error reading palette from file. Palette calibration needed")
                        self._palette_calibration()
                        utilities.save_palette_to_file("palette.txt", self._palette)

            else:
                speaker.speak("Printing single color image")
                print("\nPrinting single color image...")

            binarized, img_x, img_y = utilities.binarize_image(path, self._x_res, self._y_res, multicolor,
                                                               self._palette)
        else:
            binarized, img_x, img_y = utilities.generate_and_binarize_test_image(self._pixel_size)
            speaker.speak("Printing test page")
            print("\nPrinting test page...")

        quick_calibration = False
        self._num_of_colors = len(self._palette // 3)
        self._palette_color_names = utilities.generate_palette_color_names(self._palette)

        for layer, i in zip(binarized, range(1, self._num_of_colors)):
            speaker.speak("Insert a {} pen and press the touch sensor".format(self._palette_color_names[i]))
            self._touch.wait_for_pressed()
            self._pen_calibration(quick_calibration)

            p_codes = utilities.binarized_image_to_p_codes(layer, img_x, img_y, self._padding_left)
            if self._interpret_p_codes(p_codes):
                break

            self._paper_scroll(self._y_res)
            self._fb_motor.reset()
            self._ud_motor.reset()
            self._lr_motor.reset()
            quick_calibration = True

        speaker = Sound()
        speaker.speak("Printing finished")
        print("Printing finished")
