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
  itoo = {}
  otoi = {}
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
        otoi[opcode(name, i*16+j)] = cell.string
        if cell.string not in itoo or (documented and not itoo[cell.string][1]):
            itoo[cell.string] = (opcode(name, i*16+j), documented)
        #print("%s -> %s" % (cell.string, opcode(name, i*16+j)))
  return itoo, otoi

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

def merge_opcodes(dict1, dict2):
    """Merge two dicts containing opcode->instruction mapping.

    By design, duplicate opcode shouldn't happen.
    """
    return {**dict1, **dict2}

with open("index.html") as f:
    soup = BeautifulSoup(f, 'html.parser')
    table_name = ""
    instruction_to_opcode = {}
    opcode_to_instruction = {}
    for tag in soup.descendants:
      if tag.name == 'h3':
        #print(tag.string)
        table_name = tag.string
      if tag.name == 'table':
        itoo, otoi = parse_table(table_name, tag)
        instruction_to_opcode = merge_instructions(instruction_to_opcode, itoo)
        opcode_to_instruction = merge_opcodes(opcode_to_instruction, otoi)
    with open("all_instructions.txt", "w") as ff:
        for instr, code in instruction_to_opcode.items():
          print("%s -> %s" % (instr, code[0]), file=ff)
    with open("all_opcodes.txt", "w") as ff:
        for code, instr in opcode_to_instruction.items():
          print("%s -> %s" % (code, instr), file=ff)
