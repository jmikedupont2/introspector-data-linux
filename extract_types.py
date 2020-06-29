
import json
import pprint
from collections import Counter

identifier_field = "_id"
type_field = "_type"

known= [identifier_field,type_field]

types = Counter()
pairs = Counter()

data = {}
from itertools import combinations,permutations

# read in the file and copy the data and create the first type layer
with open("linux_clean_formatted_compact.json") as fi:
    for li in fi:
        row = json.loads(li)
        type_name = row[type_field]
        _id = row[identifier_field]
        del row[identifier_field]
        del row[type_field]
        for f in ('srcp','chain','_string_len',
                  'scpe'):
            if f in row:
                del row[f] 
        field_list = list(sorted(row.keys()))
#        field_list.insert(0, type_name)

#        
        types[str(field_list)] += 1        

for p in types.most_common(10000):
    field_list = eval(p[0])
    count = p[1]
    for p in combinations(field_list, 2):
        pairs[str(p)] += count
    for p in combinations(field_list, 3):
        pairs[str(p)] += count
    for p in combinations(field_list, 4):
        pairs[str(p)] += count
for p in pairs.most_common(10):
    print(p)
