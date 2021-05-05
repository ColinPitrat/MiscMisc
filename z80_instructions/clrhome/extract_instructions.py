#!/usr/bin/python
# -*- coding: utf8 -*-"

from bs4 import BeautifulSoup

def prefix(name):
  if name == "Main instructions":
    return "0x"
  if name == "Extended instructions (ED)":
    return "0xed"
  if name == "Bit instructions (CB)":
    return "0xcb"
  if name == "IX instructions (DD)":
    return "0xdd"
  if name == "IX bit instructions (DDCB)":
    return "0xddcb"
  if name == "IY instructions (FD)":
    return "0xfd"
  if name == "IY bit instructions (FDCB)":
    return "0xfdcb"
  raise RuntimeError("Unknown table '%s'" % name)

def opcode(name, val):
    padding = ""
    if val < 16: padding = "0";
    return prefix(name) + padding + hex(val)[2:]

def parse_table(name, tag):
  result = {}
  first_row = True
  for row in tag.children:
    if row.name != "tr":
      continue
    if first_row:
      first_row = False
      continue
    j = -1
    i = -1
    for cell in row.children:
      if cell.name == "th":
        i = int(cell.string, 16)
      if cell.name != "td":
        continue
      j += 1
      documented = True
      try:
        if 'un' in cell['class']:
          documented = False
      except KeyError:
        pass
      if cell.string:
        if cell.string not in result or (documented and not result[cell.string][1]):
            result[cell.string] = (opcode(name, i*16+j), documented)
        #print("%s -> %s" % (cell.string, opcode(name, i*16+j)))
  return result

def merge_instructions(dict1, dict2):
    """Merge two dicts containing instruction->(opcode,type) mapping.

    In case of duplicate instructions:
     - Documented instructions are preferred to documented ones.
     - Instructions from dict 1 are preferred to instructions from dict 2
    """
    for k in dict2:
        if k in dict1:
            if not dict1[k][1] and dict2[k][1]:
                dict1[k] = dict2[k]
        else:
            dict1[k] = dict2[k]
    return dict1

with open("index.html") as f:
    soup = BeautifulSoup(f, 'html.parser')
    table_name = ""
    instruction_to_opcode = {}
    for tag in soup.descendants:
      if tag.name == 'h3':
        #print(tag.string)
        table_name = tag.string
      if tag.name == 'table':
        instruction_to_opcode = merge_instructions(instruction_to_opcode, parse_table(table_name, tag))
    for instr, code in instruction_to_opcode.items():
      print("%s -> %s" % (instr, code[0]))
