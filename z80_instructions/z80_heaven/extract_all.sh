#!/bin/bash

rm instructions-set*
wget wget http://z80-heaven.wikidot.com/instructions-set
for url in `grep "instructions-set:" instructions-set | cut -d '"' -f 2`
do
  wget http://z80-heaven.wikidot.com$url
done
python3 extract_instructions.py > z80_all.asm
