#!/usr/local/bin/python3

import re
import sys

def display_help():
    print("Parses one or more latex files for citations, then outputs a list of the")
    print("citation keys. Input can be via a list of files or from stdin;")
    print("output is to stdout.\n")
    print("Usage:")
    print("  bibtally.py file1.tex file2.tex file3.tex")
    

def get_keys(s):
    s = re.findall('[^\s,]+',s)
    return s


def strip_comments(t):
    if t[0] == "%":
        r = ""
    else:
        tl = t.split('%')
        r = ""
        for i in tl:
            if len(i) > 0:
                if i[0] != "%" or r[-1] == "//":
                    r = r + i
                else:
                    break
    return r
    

dat = []

if len(sys.argv) > 1:
    if("-h" in sys.argv or "--help" in sys.argv):
        display_help()
        exit(0)
    else:
        inpTex = []
        for fname in sys.argv[1:]:
            with open(fname) as f:
                inpTex.extend(f.readlines())
else:
    inpTex = sys.stdin.readlines()

oneline = ""
for line in inpTex:
    line = strip_comments(line)
    oneline = oneline + line.rstrip('\n')


# finds all citations using the cite key
matches = re.findall('\\cite[tp]?(?!\s)\[?.*?\]?\{([^\}]+)\}',oneline)

for m in matches:
    # extracts citation keys and splits out whitespace, commas, and cite command
    keys = get_keys(m)
    for k in keys:
        # finally, check to see if it is non-empty and unique, and if so, add it to the list
        if k and not re.search("\s",k) and not k in dat:
            dat.append(k)

dat.sort()
for key in dat:
    print(key)