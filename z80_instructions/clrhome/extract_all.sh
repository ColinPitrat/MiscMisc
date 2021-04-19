#!/bin/bash

rm index.html
wget https://clrhome.org/table/
python3 extract_instructions.py > all_instructions.txt

sed 's/ ->.*//' all_instructions.txt | sed 's/\*\*/$1729/' | sed 's/\*/$42/' > z80_test_all.asm
