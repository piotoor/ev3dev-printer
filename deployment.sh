#!/bin/bash

scp main.py printer.py utilities.py reset.py robot@10.42.0.3:/home/robot/
scp -r test_images robot@10.42.0.3:/home/robot/