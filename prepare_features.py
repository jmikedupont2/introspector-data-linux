import json
import pprint

identifier_field = "_id"
type_field = "_type"

known= [identifier_field,type_field]

# determine the relationship between rows
id_to_type = {}

data = {}

def calculate_types(_data, level_name, target_level):
    # replace for each field the id of the field with the type of its value
    for _id in _data:
        row = data[_id]
        ftype = {}
        type_name = row[type_field]

        for k in row:
            if k in known:
                continue# skip
            v = row[k]

            if isinstance(v,str):
                if v in _data:
                    ftype[k] = id_to_type[v][level_name]
                else:
                    ftype[k] = "string"
            else:
                ftype[k] = str(type(v))

        type_string = { type_name : ftype }
                
        if _id not in id_to_type:
            id_to_type[_id] = { target_level : type_string }
        else:
            id_to_type[_id][target_level] = type_string


# read in the file and copy the data and create the first type layer
with open("linux_clean_formatted_compact.json") as fi:
    for li in fi:
        row = json.loads(li)
        type_name = row[type_field]
        _id = row[identifier_field]
        # save the row for second pass
        data[_id] = dict(row)        
        # remove all known fields
        for k in known:
            del row[k]            
        fields =list(row.keys())
        type_string = { type_name : fields }
        id_to_type[_id]  = { "level_1" : type_string }


calculate_types(data, level_name="level_1", target_level="level_2")
calculate_types(data, level_name="level_2", target_level="level_3")
calculate_types(data, level_name="level_3", target_level="level_4")

        
# given a row of one type, what is the maximum number of fields it will have, how many occur togeter.

#pprint.pprint(id_to_type)
for x in id_to_type:
    for l in id_to_type[x]:
        v = id_to_type[x][l]
        print(json.dumps(v))

# python3 prepare_features.py | sort | uniq -c  |sort -n > common_types.txt
