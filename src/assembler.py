#!/usr/bin/python3
from hackParser import parse

def assemble(script):
    symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
        "R0": "0",
        "R1": "1",
        "R2": "2",
        "R3": "3",
        "R4": "4",
        "R5": "5",
        "R6": "6",
        "R7": "7",
        "R8": "8",
        "R9": "9",
        "R10": "10",
        "R11": "11",
        "R12": "12",
        "R13": "13",
        "R14": "14",
        "R15": "15"
    }
    redo = []
    output = []
    for line in script:
        uncommented, _, _comment = line.partition("//") # remove inline comments
        stripped: str = uncommented.strip() # remove leading and trailing whitespace could possibly just replace() all
        if not stripped:
            continue
        elif stripped.startswith("@"):
            if stripped[1:].isdigit():
                output.append(format(int(stripped[1:]), '0>16b'))
            else:
                if stripped[1:] in symbols:
                    output.append(format(int(symbols[stripped[1:]]), '0>16b'))
                else:
                    redo.append(len(output))
                    output.append(stripped[1:])
        elif stripped.startswith("(") and stripped.endswith(")"):
            symbol = stripped[1:-1]
            symbols[symbol] = str(len(output))
        else: # command
            comp, dest, jump = parse(stripped)
            output.append("111{comp}{dest}{jump}".format(comp=comp, dest=dest, jump=jump))
    
    current = 16
    for index in redo:
        if output[index] in symbols:
            output[index] = format(int(symbols[output[index]]), '0>16b')
        else:
            symbols[output[index]] = str(current)
            output[index] = format(current, '0>16b')
            current += 1
    return output