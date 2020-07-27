import json
import pprint
def visit_type(row):
    if not isinstance(row,dict):
        return str(type(row))
    if '_type' not in row:
        #pprint.pprint(row)
        pass
        
    t=  row['_type']
    if t == 'record_type':
        return record(row)
        
    elif t == 'type_decl':
        return (t,type_decl(row))
    else:
        return t

def type_decl(row, visit=visit_type):
    typedef_name= "unknown"
    
    if '_string' in row:
        typedef_name = row['_string']
            
    if '__type' in row:
        dtype = row['__type']
        return (typedef_name,visit(dtype) )
    return "TODO"


def visit_type2(row):
    if not isinstance(row,dict):
        return str(type(row))
    if '_type' not in row:
        #pprint.pprint(row)
        pass
        
    t=  row['_type']
    if t == 'record_type':
        return "record_type:" +str(record_name(row))
        
    elif t == 'type_decl':
        return (t,type_decl(row, visit_type2))
    else:
        return t
    
def record_name(row1):
    name = "None"
    if '_string' in row1:
        name = row1['_string']
        return name
    
    if '__ptd' in row1:
        row = row1['__ptd']
    elif '__type' in row1:
        row = row1['__type']
    else:
        #pprint.pprint(row1)
        return row1.keys()

    if '_string' in row:
        name = row['_string']
        return name
    return "unknown"

def record(row1):
    name = "None"
    if '__ptd' in row1:
        row = row1['__ptd']
    elif '__type' in row1:
        row = row1['__type']
    else:
        #pprint.pprint(row1)
        return row1.keys()
        
    if '_string' in row:
        name = row['_string']
            
    fields = []
    if '__flds' in row:
        flds = row['__flds']
        for f in flds:
            fname = "unknown"
            ftype = fname
            if '_string' in f:
                fname = f['_string']
            if '__type' in f:
                ftype = visit_type2(f['__type'])
                
            fields.append(str([fname, ftype]))

    fstr =",".join(fields)
    return ' '.join([name, fstr])

    
    
with open("record_types.json") as fi:
    for li in fi:
        row = json.loads(li)
        print(visit_type(row))

