#!/usr/bin/env bash

for test in tests/inputs/*; do
  ./build/hopfield $test
  python3 input_to_output.py
  mv result.png "tests/outputs/$(basename "$test" .dat).png"
  mv input_end.dat "tests/outputs/$(basename "$test" .dat).out"
  rm input_start.dat
done
