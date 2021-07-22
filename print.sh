#!/bin/bash

if(($#==2));
then
  scp "$1" robot@10.42.0.3:/home/robot/
  # shellcheck disable=SC2029
  ssh robot@10.42.0.3 "python3 main.py -f $1 -p $2 | tee log.txt"
elif(($#==1));
then
  # shellcheck disable=SC2029
  ssh robot@10.42.0.3 "python3 main.py -p $1 | tee log.txt"
else
  ssh robot@10.42.0.3 "python3 main.py -h  | tee log.txt"
fi
