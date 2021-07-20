#!/bin/bash

if(($#==2));
then
  scp "$2" robot@10.42.0.3:/home/robot/
  ssh robot@10.42.0.3 "python3 main.py -f \$1 -p \$2"
elif(($#==1));
then
  ssh robot@10.42.0.3 "python3 main.py -p $1"
else
  ssh robot@10.42.0.3 "python3 main.py -h"
fi
