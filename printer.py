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
        self.touch = TouchSensor(INPUT_1)
        self.color = ColorSensor(INPUT_4)
        self.color.mode = 'COL-COLOR'
        self.fb_motor = LargeMotor(OUTPUT_C)
        self.lr_motor = LargeMotor(OUTPUT_B)
        self.ud_motor = Motor(OUTPUT_A)

        self.x_res = utilities.MAX_X_RES / int(pixel_size)
        self.y_res = utilities.MAX_Y_RES / int(pixel_size)
        self.padding_left = utilities.MAX_PADDING_LEFT / int(pixel_size)
        self.padding_right = utilities.MAX_PADDING_RIGHT / int(pixel_size)
        self.is_pen_up = True
        self.pen_calibrated = False

        self.ud_ratio = 5
        self.fb_ratio = 4
        self.lr_ratio = 1
        self.pen_up_val = -3 * self.ud_ratio
        self.pen_down_val = -self.pen_up_val
        self.pen_up_down_speed = 10
        self.pen_left_speed = 20
        self.pen_right_speed = 20
        self.paper_scroll_speed = 20

        self.palette = []
        self.palette_color_names = ["black"]
        self.num_of_colors = 2
        self.pixel_size = pixel_size
        self.p_codes = []
        self.current_line = 0

    def pen_up(self, val):
        print("{} {}".format('PEN_UP', val))
        if val > 0:
            self.ud_motor.on_for_degrees(self.pen_up_down_speed, val * self.pen_up_val)
            self.is_pen_up = True

    def pen_down(self, val):
        print("{} {}".format('PEN_DOWN', val))
        if val > 0:
            self.ud_motor.on_for_degrees(self.pen_up_down_speed, val * self.pen_down_val)
            self.is_pen_up = False

    def pen_left(self, val):
        print("{} {}".format('PEN_LEFT', val))
        if val > 0:
            self.lr_motor.on_for_degrees(self.pen_left_speed, int(self.pixel_size) * val * self.lr_ratio)

    def pen_right(self, val):
        print("{} {}".format('PEN_RIGHT', val))
        if val > 0:
            self.lr_motor.on_for_degrees(self.pen_right_speed, -int(self.pixel_size) * val * self.lr_ratio)

    def paper_scroll(self, val):
        print("{} {}".format('SCROLL', val))
        if val > 0:
            if val == 1:
                self.current_line += val
                print("-------------- Line {} --------------".format(self.current_line))
            self.fb_motor.on_for_degrees(self.paper_scroll_speed, int(self.pixel_size) * val * self.fb_ratio)

    def finish_calibration(self):
        self.pen_calibrated = True

    def palette_calibration(self):
        curr_color_mode = self.color.mode
        self.color.mode = 'RGB-RAW'

        calibration_done = False

        speaker = Sound()
        palette = []
        self.fb_motor.reset()
        self.fb_motor.on(5)
        initial_vals = prev_vals = self.color.rgb
        epsilon = 10
        new_color = True

        while not calibration_done and not self.touch.value():
            vals = self.color.rgb
            delta_prev_vals = (abs(vals[0] - prev_vals[0]), abs(vals[1] - prev_vals[1]), abs(vals[2] - prev_vals[2]))
            delta_init_vals = (
                abs(vals[0] - initial_vals[0]), abs(vals[1] - initial_vals[1]), abs(vals[2] - initial_vals[2]))

            if len(palette) > 0:
                delta_last_vals = (
                    abs(vals[0] - palette[-1][0]), abs(vals[1] - palette[-1][1]), abs(vals[2] - palette[-1][2]))
            else:
                delta_last_vals = (3 * epsilon, 3 * epsilon, 3 * epsilon)

            if (len(palette) > 1 and max(delta_init_vals) <= 2 * epsilon and new_color) or abs(
                    self.fb_motor.position) > 360 * self.fb_ratio:
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
                self.palette.append(y)

        self.color.mode = curr_color_mode
        self.fb_motor.reset()
        utilities.save_palette_to_file("palette.txt", self.palette)

    def pen_calibration(self, quick_calibration):
        speaker = Sound()

        if quick_calibration:
            speaker.speak("Quick calibration")
            print("Quick calibration...")
        else:
            speaker.speak("Calibrating")
            print("Calibrating...")
            btn = Button()

            self.lr_motor.reset()
            self.ud_motor.reset()
            self.fb_motor.reset()

            self.lr_motor.on_for_degrees(self.pen_left_speed, self.x_res * self.pixel_size * self.lr_ratio)
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
            print("Adjust pen height...")

            while not self.pen_calibrated:
                self.lr_motor.on_for_degrees(self.pen_right_speed, -100 * self.pixel_size * self.lr_ratio)
                self.lr_motor.on_for_degrees(self.pen_left_speed, 100 * self.pixel_size * self.lr_ratio)
                time.sleep(1)
                if btn.up:
                    self.pen_up(1)
                elif btn.down:
                    self.pen_down(1)
                elif btn.right:
                    self.finish_calibration()
                elif btn.left:
                    self.pen_down(4)

            self.lr_motor.reset()

        if not self.is_pen_up:
            self.pen_up(1)
        self.pen_left(self.x_res)

        for _ in range(2):
            self.pen_right(self.x_res)
            self.pen_left(self.x_res)
        for _ in range(8):
            self.pen_right(self.padding_left)
            for _ in range(int(self.x_res)):
                self.pen_right(1)
            self.pen_left(self.x_res + self.padding_left)
        self.lr_motor.reset()

        speaker.speak("Insert a blank piece of paper and press the touch sensor")
        self.touch.wait_for_pressed()
        self.fb_motor.on(5)
        val = 0
        print("Scrolling the piece of paper to its starting position...")
        while self.colors[val] == 'black':
            val = self.color.value()

        self.fb_motor.reset()
        print("Calibration done")

    def interpret_p_codes(self, p_codes):
        btn = Button()
        speaker = Sound()
        self.current_line = 0
        abort = False

        print("---------- p_codes:----------")
        print("-------------- Line {} --------------".format(self.current_line))
        for x in p_codes:
            if btn.down:
                speaker.speak("Aborting")
                print("\nAborting...")
                abort = True
                break

            if x[0] == utilities.Command.PEN_UP:
                if not self.is_pen_up:
                    self.pen_up(x[1])

            elif x[0] == utilities.Command.PEN_DOWN:
                if self.is_pen_up:
                    self.pen_down(x[1])

            elif x[0] == utilities.Command.PEN_RIGHT:
                self.pen_right(x[1])

            elif x[0] == utilities.Command.PEN_LEFT:
                self.pen_left(x[1])

            elif x[0] == utilities.Command.SCROLL:
                self.paper_scroll(x[1])

        if not self.is_pen_up:
            self.pen_up(1)
        self.ud_motor.stop()

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
                    self.palette_calibration()
                else:
                    try:
                        self.palette = utilities.read_palette_from_file("palette.txt")
                        # validate size of palette
                    except IOError:
                        print("Error reading palette from file. Palette calibration needed")
                        speaker.speak("Error reading palette from file. Palette calibration needed")
                        self.palette_calibration()
                        utilities.save_palette_to_file("palette.txt", self.palette)

            else:
                speaker.speak("Printing single color image")
                print("\nPrinting single color image...")

            binarized, img_x, img_y = utilities.binarize_image(path, self.x_res, self.y_res, multicolor,
                                                               self.palette)
        else:
            binarized, img_x, img_y = utilities.generate_and_binarize_test_image(self.pixel_size)
            speaker.speak("Printing test page")
            print("\nPrinting test page...")

        quick_calibration = False
        self.num_of_colors = len(self.palette // 3)
        self.palette_color_names = utilities.generate_palette_color_names(self.palette)

        for layer, i in zip(binarized, range(1, self.num_of_colors)):
            speaker.speak("Insert a {} pen and press the touch sensor".format(self.palette_color_names[i]))
            self.touch.wait_for_pressed()
            self.pen_calibration(quick_calibration)

            p_codes = utilities.binarized_image_to_p_codes(layer, img_x, img_y, self.padding_left)
            if self.interpret_p_codes(p_codes):
                break

            self.paper_scroll(self.y_res)
            self.fb_motor.reset()
            self.ud_motor.reset()
            self.lr_motor.reset()
            quick_calibration = True

        speaker = Sound()
        speaker.speak("Printing finished")
        print("Printing finished")
