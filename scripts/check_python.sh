#!/bin/bash

if [ "$#" -eq 0 ]; then
  echo "Error: Need provide direct: --up or --down"
  exit 1
fi

arg=$1

valid_args=(--up --down)
is_valid=0

for value in "${valid_args[@]}"; do
  if [ "$arg" == "$value" ]; then
    is_valid=1
    break
  fi
done

if [ "$is_valid" -ne 1 ]; then
  echo "Invalid argument - '$arg'."
  exit 1
fi

declare -a python_commands
python_commands=(python python3 py py3)

for value in "${python_commands[@]}"
do
    if type $value 1> /dev/null 2> /dev/null;
    then
        ${value} -m scripts $arg
    else 
        continue
    fi
done
