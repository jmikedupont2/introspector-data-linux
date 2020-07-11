
import json
import pprint
from flatten_dict import flatten


identifier_field = "_id"
type_field = "_type"

known= [identifier_field,type_field]

# determine the relationship between rows
id_to_type = {}

# extract the data for each type
id_to_data = {}

data = {}

def calculate_types(_data, level_name, target_level):
    # replace for each field the id of the field with the type of its value
    for _id in _data:
        row = data[_id]
        ftype = {}
        type_name = row[type_field]

        row2 = {}
        
        for k in row:
            if k in ("chan","chain","type","ref","unql",'size',"min","max"):  #skip cross links
                continue
            v = row[k]
            if k in known:
                row2[k] = row[k]
            else:
                if isinstance(v,str):
                    if v in _data:
                        ftype[k] = id_to_type[v][level_name]
                        row2[k] = id_to_data[v][level_name]
                    else:
                        ftype[k] = "string"
                        row2[k]= row[k]
                elif isinstance(v,int):
                    ftype[k] = "pythonint"
                elif isinstance(v,dict):
                    if "name" in v:
                        ftype[k] = "named_node"
                    else:
                        pprint.pprint(v)
                        raise Exception(v)
                        ftype[k] = "dict"
                else:
                    raise Exception(str(type(v)))
                    ftype[k] = str(type(v))
                    row2[k]= row[k]

        type_string = { type_name : ftype }
                
        if _id not in id_to_type:
            id_to_type[_id] = { target_level : type_string }
        else:
            id_to_type[_id][target_level] = type_string
            
        if _id not in id_to_data:
            id_to_data[_id] = { target_level : row2 }
        else:
            id_to_data[_id][target_level] = row2

def calculate_chains(_data, level_name, target_level):
    # loop over all the chains of interest
    for _id in _data:
        row = data[_id]
        ftype = {}
        type_name = row[type_field]

        row2 = {}
        
        for k in row:
            if k in ("chan","chain"):  #
                v = row[k]

                if isinstance(v,str):
                    if v in _data:
                        ftype[k] = id_to_type[v][level_name]
                        row2[k] = id_to_data[v][level_name]




# read in the file and copy the data and create the first type layer
with open("linux_clean_formatted_compact.json") as fi:
    for li in fi:
        row = json.loads(li)
        type_name = row[type_field]
        _id = row[identifier_field]
        # save the row for second pass
        data[_id] = dict(row)        
        # remove all known fields

        #for k in known:
        #    del row[k]            
        fields ="_".join(list(sorted(row.keys())))
        type_string = { type_name : fields }
        id_to_type[_id]  = { "level_1" : type_string }
        
        id_to_data[_id]  = { "level_1" : row }        


calculate_types(data, level_name="level_1", target_level="level_2")
#calculate_types(data, level_name="level_2", target_level="level_3")
#calculate_types(data, level_name="level_3", target_level="level_4")


calculate_chains(data, level_name="level_1", target_level="level_2a")

def underscore_reducer(k1, k2):
    if k1 is None:
        return k2
    else:
        return k1 + "_" + k2
        
# given a row of one type, what is the maximum number of fields it will have, how many occur togeter.

#pprint.pprint(id_to_type)
for x in id_to_type:
    for l in id_to_type[x]:

        tv = id_to_type[x][l]
        v = id_to_data[x][l]
        v['_level'] = l

        flatten_type = flatten(tv, reducer=underscore_reducer)

        ordered = sorted(list(flatten_type.keys()))
        typestring =  "_".join([
            k + str(flatten_type[k]) for k in ordered
        ])

        v['_type2'] = typestring
        flatten_data = flatten(v, reducer=underscore_reducer)
                
        print(json.dumps(flatten_data))

# python3 prepare_features.py | sort | uniq -c  |sort -n > common_types.txt
