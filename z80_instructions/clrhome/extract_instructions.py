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
    return "0xdd"
  if name == "IY bit instructions (FDCB)":
    return "0xddcb"
  raise RuntimeError("Unknown table '%s'" % name)

def opcode(name, val):
    return prefix(name) + hex(val)[2:]

def parse_table(name, tag):
  first_row = True
  for row in tag.children:
    if row.name != "tr":
      continue
    if first_row:
      first_row = False
      continue
    j = 0
    i = -1
    for cell in row.children:
      if cell.name == "th":
        i = int(cell.string, 16)
      if cell.name != "td":
        continue
      if cell.string:
        print("%s -> %s" % (cell.string, opcode(name, i*16+j)))
      j += 1

with open("index.html") as f:
    soup = BeautifulSoup(f, 'html.parser')
    table_name = ""
    for tag in soup.descendants:
      if tag.name == 'h3':
        #print(tag.string)
        table_name = tag.string
      if tag.name == 'table':
        parse_table(table_name, tag)
