#!/usr/local/bin/python3

import re
import sys


def strip_comments(t):
    if t[0] == "%":
        r = ""
    else:
        tl = t.split('%')
        r = ""
        for i in tl:
            if i[0] != "%" or r[-1] == "//":
                r = r + i
            else:
                break
    return r

def output_usage(name):
    print("Usage:", name, " <input_bibtex_file> <list_of_keys>", file=sys.stderr)
    print("Extracts bibtex records matching list_of_keys from the input file. \nThe list of keys is optional; if omitted, it is read from stdin", file=sys.stderr)
    sys.exit(0)
	
keys = []
if len(sys.argv) == 1:
    output_usage(sys.argv[0])
else:
    with open(sys.argv[1]) as f:
        inpBib = f.readlines()
    if len(sys.argv) == 2:
        keys = [line.rstrip() for line in sys.stdin.readlines()]
    else:
        keys = [line.rstrip() for line in open(sys.argv[2])]

output = False
for line in inpBib:
    sLine = strip_comments(line)
    
    # this will match the beginning of a citation key
    match = re.search('@[^\{]+\{([^,]+),', sLine)
    
    # next, check to see if the key is one we want
    if match:
        if match.group(1) in keys:
            output = True
        else:
            # this will reset it to false once we come to a non-matching citation
            output = False
        
    if output:
        print(line,end="")