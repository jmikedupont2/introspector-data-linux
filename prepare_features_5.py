
import json
import pprint
from flatten_dict import flatten
import collections

identifier_field = "_id"
type_field = "_type"

known= [identifier_field,type_field]

data = {}
counter=collections.Counter()
from type_name_extractor import extract_name

def calculate_types(_data, level_name, target_level):
    # replace for each field the id of the field with the type of its value
    for _id in _data:
        row = data[_id]
        ftype = {}
        type_name = row[type_field]

        row2 = {}
        
        for k in row:
 
            v = row[k]
            if k in known:
                row2[k] = row[k]
            else:
                if isinstance(v,str):
                    if v in _data:
                        to_type = _data[v][type_field]

                        fname = k
                        #for d in [str(x) for x in range(0,10)]:
                        #    fname = fname.replace(str(d),"")
                        fname = fname.replace(" ","").replace(":","")

                        d = tuple([type_name, fname, to_type])
                        
                        counter[d] += 1



# read in the file and copy the data and create the first type layer
with open("linux_clean_formatted_compact.json") as fi:
    for li in fi:
        row = json.loads(li)
        type_name = row[type_field]
        _id = row[identifier_field]
        # save the row for second pass
        data[_id] = dict(row)        



calculate_types(data, level_name="level_1", target_level="level_2")
for n in counter:
    v = counter[n]
#    print("\t".join(n) + "\t" + str(v))
    fname = n[1]
    print("\t".join([
        n[0],
        fname,
        n[2],        
        str(v)]))


