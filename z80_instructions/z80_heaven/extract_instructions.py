#!/usr/bin/python
# -*- coding: utf8 -*-"

import os

from bs4 import BeautifulSoup

def snippets_patches(code):
    # Some examples use +d which is inavlid because d is a register
    code = code.replace('IX+d', 'IX+n')
    code = code.replace('IY+d', 'IY+n')
    code = code.replace('Note: Undocumented', 'Note: Undocumented ; pasmo does not support this')
    code = code.replace('undocumented command', 'undocumented command ; pasmo does not support this')
    return code

print("n equ $00")
print("nn: dw $0000")
print("imm8: dw $00")
print("label:")
for fn in os.listdir('.'):
    if fn.startswith('instructions-set:'):
      instruction=fn.split(':')[1]
      #print(" == %s ==" % instruction)
      last_code = ""
      if instruction.lower() == 'ld':
        for r1 in ['a', 'b', 'c', 'd', 'e', 'h', 'l']:
            for r2 in ['a', 'b', 'c', 'd', 'e', 'h', 'l']:
                print("ld %s, %s" % (r1, r2))
        for r in ['i', 'r', '(bc)', '(de)', '(nn)']:
            print("ld a, %s" % r)
        for r1 in ['a', 'b', 'c', 'd', 'e']:
            for r2 in ['ixh', 'ixl', 'iyh', 'iyl', '(hl)', '(ix+n)', '(iy+n)', 'n']:
                print("ld %s, %s" % (r1, r2))
        for r1 in ['ixh', 'ixl', 'iyh', 'iyl']:
            for r2 in ['a', 'b', 'c', 'd', 'e', 'n']:
                print("ld %s, %s" % (r1, r2))
        for r1 in ['ixh', 'ixl']:
            for r2 in ['ixh', 'ixl']:
                print("ld %s, %s" % (r1, r2))
        for r1 in ['iyh', 'iyl']:
            for r2 in ['iyh', 'iyl']:
                print("ld %s, %s" % (r1, r2))
        for r1 in ['bc', 'de', 'hl', 'sp', 'ix', 'iy']:
            for r2 in ['nn', '(nn)']:
                print("ld %s, %s" % (r1, r2))
        for r2 in ['hl', 'ix', 'iy']:
            print("ld sp, %s" % r2)
        for r1 in ['(bc)', '(de)', '(hl)', '(ix+n)', '(iy+n)', '(nn)']:
            print("ld %s, a" % r1)
        for r1 in ['(hl)', '(ix+n)', '(iy+n)']:
            for r2 in ['b', 'c', 'd', 'e', 'h', 'l']:
                print("ld %s, %s" % (r1, r2))
        for r2 in ['bc', 'de', 'hl', 'sp', 'ix', 'iy']:
            print("ld (nn), %s" % r2)
        continue
      if instruction.lower() == 'djnz':
        print("djnz label")
        continue
      if instruction.lower() == 'im':
        print("im 0")
        print("im 1")
        print("im 2")
        continue

      if instruction.lower() == 'sbc':
        # We need a label at the beginning of the SBC section so that it's not too far for a relative jump
        print("NN:")
        # Note: no continue on purpose, we want the normal processing for sbc here on top of the label
      with open(fn) as f:
        soup = BeautifulSoup(f, 'html.parser')
        in_allowed_instructions = False
        found = False
        for tag in soup.descendants:
          if tag.string and tag.string.lower() in ['allowed instructions', 'acceptable inputs']:
            in_allowed_instructions = True
          elif tag.name == 'h3' or tag.name == 'h2':
            if in_allowed_instructions:
              if not found and last_code:
                print(snippets_patches(last_code))
                found = True
              in_allowed_instructions = False
          if tag.name == 'code':
            #print("DEBUG: tag: %s -> %s" % (tag.name, tag.string))
            if in_allowed_instructions:
              print(snippets_patches(tag.string))
              found = True
            else:
              last_code = tag.string
        if not found:
          print(instruction)
