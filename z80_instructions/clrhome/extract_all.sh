#!/bin/bash

rm index.html
wget https://clrhome.org/table/
python3 extract_instructions.py > all_instructions.txt

sed 's/ ->.*//' all_instructions.txt | sed 's/\*\*/$1729/g' | sed 's/\*/$42/g' > z80_test_all.asm
