# naming convention extractor

splitters = [
    '_____',
    '____',
    '___',
    '__',
    '_',
    ' ',
    '*',
    '.',
    "/"
]

import collections
# camelcase
chars = collections.Counter()

with open("names.txt") as fi:
    for l in fi:
        l = l.strip()

        parts = { l : 1}
        
        for s in splitters:
            for p in dict(parts):
                for s2 in p.split(s):
                    if s2 not in parts:
                        parts[s2] =1
                        if p in parts:
                            del[parts[p]]
            
        for c in parts:
            chars[c]+=1
            
#        for (c,c2) in enumerate(l):
#            chars[l[c-1] + l[c]]+=1          
#            if c > 1:
#                chars[l[c-2] + l[c-1] + l[c] ]+=1
#            if c > 2:
#                chars[l[c-3] + l[c-2] + l[c-1] + l[c] ]+=1
#            if c > 3:
#                chars[l[c-4] + l[c-3] + l[c-2] + l[c-1] + l[c] ]+=1
            

for x in chars.most_common(200):
    print(x)
            
