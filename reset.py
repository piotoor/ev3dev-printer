#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, Motor


def reset():
    fb_motor = LargeMotor(OUTPUT_C)
    lr_motor = LargeMotor(OUTPUT_B)
    ud_motor = Motor(OUTPUT_A)
    fb_motor.stop()
    lr_motor.stop()
    ud_motor.stop()


if __name__ == '__main__':
    reset()
