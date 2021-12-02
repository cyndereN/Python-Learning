def get_unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

# uniq 
file = args[0]
with open(file) as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = sorted(set(lines), key=lines.index)
    if len(options) == 1 and options[0] == "i":
        lines_l = [line.lower() for line in lines]
        lines_l = sorted(set(lines_l), key=lines_l.index)
        for line in lines:
            if line.lower() in lines_l:
                lines_l.remove(line.lower())
            else:
                lines.remove(line)
    for line in lines:
        out.append(line + "\n")

import itertools, operator
import sys

if sys.hexversion < 0x03000000:
    mapper= itertools.imap # 2.4 ≤ Python < 3
else:
    mapper= map # Python ≥ 3

def sort_uniq(sequence):
    return mapper(
        operator.itemgetter(0),
        itertools.groupby(sorted(sequence)))