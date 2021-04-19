# MiscMisc

Some random unclassifiable stuff worth keeping somewhere for reference.

## z80_instructions

Some script to fetch all valid z80 assembly instructions from z80-heaven and
clrhome.org.
It also extracts all instruction -> opcode correspondence from clrhome.org.
I wrote this as an helper to implement and test TRSE (
https://github.com/leuat/TRSE) and Caprice32 (
https://github.com/ColinPitrat/caprice32)

### z80_heaven subdirectory

This is a tool that scrapes http://z80-heaven.wikidot.com/instructions-set to
produce a `z80_all.asm` test file which (hopefully) contains all z80
instructions (it seems it's not actually complete). The directory also contains
the result of the run.

Just run `make` to run the tool and `make clean` to remove the generated files.

### clrhome subdirectory

This is a tool and the data it extracts from https://clrhome.org/table/ to
produce:

 - a instruction -> opcode correspondance
 - a test file with all z80 instructions

The directory also contains the result of the run.

Just run `make` to run the tool and `make clean` to remove the generated files.
