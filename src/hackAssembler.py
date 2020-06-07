#!/usr/bin/python3
from sys import argv
from assembler import assemble

if __name__ == "__main__":
    with open(argv[1], 'r') as asm:
        output = assemble(asm.readlines())
    with open(argv[2], 'w+') as outFile:
        outFile.writelines("\n".join(output))