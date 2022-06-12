#!/bin/bash

trap break INT
for i in {1..40}
do
  gtimeout 300 python ./sat_solver.py $i
done