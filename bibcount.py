#!/usr/local/bin/python3

import re
import sys


def output_usage():
    name = sys.argv[0]
    print(name, "usage:\n")
    print("    ", name, "<latex_file.tex> <list_of_keys.txt>\n")
    print("The list of keys is optional; if missing, it will be read from stdin\n")
    sys.exit()


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



keys = []
if len(sys.argv) == 1:
    output_usage()
else:
    with open(sys.argv[1]) as f:
        inpTex = f.readlines()
    if len(sys.argv) == 2:
        keys = [line.rstrip() for line in sys.stdin.readlines()]
    else:
        keys = [line.rstrip() for line in open(sys.argv[2])]

    

# set up dictionary
maxlen = 0
dat = dict()
for k in keys:
    dat[k] = 0
    if len(k) > maxlen:
        maxlen = len(k)
        
# count the references
for line in inpTex:
    line = strip_comments(line)
    for k in keys:
    
        matches = re.findall('\\cite[tp]?(?!\s)(\[.*\])*\{[^\}]*' + k + '[^\}]*\}', line)
        dat[k] = dat[k] + len(matches)    

for k in keys:
    print(str(k).ljust(maxlen+1), str(dat[k]).ljust(3))
    
print("\nTotal number of citations: ", str(len(dat.keys())))