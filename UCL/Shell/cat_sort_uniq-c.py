import collections

c = collections.Counter()

with open('file.txt') as f:
    for text in f:
        c.update( [int(text.strip())] )

c_sorted = sorted(c.most_common())

for key, val in c_sorted:
    print val, key