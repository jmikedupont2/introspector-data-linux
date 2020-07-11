# read in count of types
import collections
from itertools import combinations,permutations
counter=collections.Counter()
with open("type_count.txt") as fi:
    for li in fi:        
        parts = li.strip().split(" ")
        count = int(parts[0])
        name = "_".join(parts[1:])
        name = name.replace(" :","_")
        name = name.replace(" ","_")
        name = name.replace(":","_")
        parts = name.split("_")
#        for p in parts:
#            counter[p] += count

        for (c,p2) in enumerate(parts):
            counter[str(parts[c-1])+","+str(p2)] += count
for x in counter:
    print("\t".join([str(x), str(counter[x])]))
            
