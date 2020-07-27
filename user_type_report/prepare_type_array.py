import json
import pprint
import collections
import pandas as pd
import numpy as np
import sys

opt_collect_normal=True
FIELDS='__scpe_rev'

usage = collections.Counter()

identifier_field = "_id"
type_field = "_type"

known= [identifier_field,type_field]
def record_type(node):
    start = node['__type']['__type']

    name = "unknown"
    if '_string' in start:
        name = start['_string']
    else:
        #print(node)
        pass
    ldata = None
    if FIELDS in start :
        
        #print( [ x for x in start[FIELDS] ] )
        data = {'struct':{
            'name': name,
            'fields' : {
                x["_string"]: "TODO" for x in start[FIELDS] 
            }
        }}

        return data
    return node

def enum_csts(node):
    #print("found")
    start = node['__type']['__type']

    name = "unknown"
    if '_string' in start:
        name = start['_string']
    else:
        #print(node)
        pass
    ldata = None
    if '__csts' in start :
        if 'chan' in start['__csts']:
            ldata = start['__csts']['chan']
    data = {'enum':{
        name : ldata
    }}
    #print(data)
    return data
    
patterns = [
    # {
    #     'node_type': 'type_decl', # __type
    #     'field': 'type',
    #     'child':{
    #         'node_type': 'enumeral_type',
    #         'field': 'type',
    #         'child': {
    #             'node_type': 'tree_list',
    #             'field': 'csts',
    #             'function' :  enum_csts,
    #         }
    #     }
    # },
    # {
    #     # match any node type
    #     'field': 'type',
    #     'child':{
    #         'node_type': 'enumeral_type',
    #         'field': 'type',
    #         'child': {
    #             'node_type': 'tree_list',
    #             'field': 'csts',
    #             'function' :  enum_csts,
    #         }
    #     }
    # },

    
    # {
    
    #     'node_type': 'enumeral_type',
    #     'field': 'type',
    #     'child': {
    #         'node_type': 'tree_list',
    #         'field': 'csts',
    #         'function' :  enum_csts,
    #     }
    # },

    {
        'node_type': 'type_decl', # __type
        'field': 'type',
        'child':{
    
            'node_type': 'record_type',
            'function' : record_type,
        }
    }

    
]

def get_field(node, field):
    pass

   #    1 bit_field_ref
   #    1 float_expr
   #    1 max_expr
   #    1 min_expr
   #    1 rdiv_expr
   #    2 bit_xor_expr
   #    2 lrotate_expr
   #    2 predecrement_expr
   #    2 preincrement_expr
   #    2 real_cst
   #    3 postdecrement_expr
   #    4 negate_expr
   #    5 bit_not_expr
   #    7 switch_expr
   #    8 compound_literal_expr
   #   10 predict_expr
   #   11 compound_expr
   #   11 save_expr
   #   11 trunc_mod_expr
   #   12 ge_expr
   #   13 truth_not_expr
   #   15 asm_expr
   #   19 minus_expr
   #   24 trunc_div_expr
   #   32 truth_orif_expr
   #   34 bit_ior_expr
   #   37 gt_expr
   #   38 array_ref
   #   38 le_expr
   #   43 lshift_expr
   #   48 truth_andif_expr
   #   63 convert_expr
   #   63 postincrement_expr
   #   68 target_expr
   #   71 mult_expr
   #   71 pointer_plus_expr
   #   80 rshift_expr
   #   87 case_label_expr
   #  143 lt_expr
   #  154 bit_and_expr
   #  179 plus_expr
   #  228 eq_expr
   #  255 string_cst
   #  277 label_expr
   #  360 result_decl
   #  364 label_decl
   #  380 goto_expr
   #  434 ne_expr
   #  575 decl_expr
   #  577 bind_expr
   #  668 cond_expr
   #  697 return_expr
   #  723 var_decl
   #  902 parm_decl
   # 1080 type_decl
   # 1103 integer_cst
   # 1105 indirect_ref
   # 1193 call_expr
   # 1294 component_ref
   # 1402 const_decl
   # 1457 nop_expr
   # 1462 modify_expr
   # 1922 addr_expr
   # 2620 field_decl
   # 4074 function_decl
   
def match_patterns_2(node, pattern):

    
    ntype = node['_type']
    if 'node_type' in pattern :
        ctype = pattern['node_type']        
        if ntype != ctype :
            #print(ntype)
            return None # no match

    if 'field' in pattern:
        cfield = "__" + pattern['field']
        if cfield in node:            
            if 'child' in pattern:
                child = pattern['child']
                node2 = node[cfield]
                #import pdb
                #pdb.set_trace()

                ntype2 = node2['_type']
                #print(ntype,ntype2)
                
                res = match_patterns_2(node2, child)
                if res :
                    return res

    if 'function' in pattern:
        return pattern['function'] # call that

    return False                    
                

def match_patterns(node):
    for pattern in patterns:
        res = match_patterns_2(node, pattern)
        if res :
            return res(node)

# all nodes
data = {}

# what type node id maps to what node id
types = {}

fields = {
    '_id': 1,
    '_type': 1, 'chain': 1, '_string': 1, '_string_len': 1, 'size': 1, 'algn': 1, 'prec': 1, 'sign': 1, 'min': 1, 'max': 1, 'unql': 1, 'domn': 1, 'tag': 1, 'bpos': 1, 'mngl': 1, 'body': 1, 'link': 1, 'prms': 1, 'cnst': 1, 'purp': 1, 'qual': 1, 'args': 1, 'argt': 1, 'used': 1, 'expr': 1, 'OP0 :': 1, 'OP1': 1, 'fn': 1, 'E0': 1, 'E1': 1, 'cond': 1, 'E2': 1, 'E3': 1, 'E4': 1, 'E5': 1, 'E6': 1, 'E7': 1, 'E8': 1, 'E9': 1, 'E10': 1, 'E11': 1, 'E12': 1, 'E13': 1, 'E14': 1, 'E15': 1, 'low': 1, 'labl': 1, 'val': 1, 'OP2': 1, 'decl': 1, 'init': 1, 'vars': 1, 'idx': 1, 'E16': 1, 'E17': 1, 'E18': 1, 'E19': 1, 'E20': 1, 'E21': 1, 'E22': 1, 'E23': 1, 'E24': 1, 'E25': 1, 'E26': 1, 'E27': 1, 'E28': 1, 'E29': 1, 'E30': 1, 'E31': 1, 'E32': 1, 'E33': 1, 'E34': 1, 'E35': 1, 'E36': 1, 'E37': 1, 'E38': 1, 'E39': 1, 'E40': 1, 'E41': 1, 'E42': 1, 'E43': 1, 'E44': 1, 'E45': 1, 'E46': 1, 'E47': 1, 'E48': 1, 'E49': 1, 'E50': 1, 'E51': 1, 'E52': 1, 'E53': 1, 'E54': 1, 'E55': 1, 'E56': 1, 'E57': 1, 'E58': 1, 'E59': 1, 'E60': 1, 'E61': 1, 'E62': 1, 'E63': 1, 'E64': 1, 'E65': 1, 'E66': 1, 'E67': 1, 'E68': 1, 'E69': 1, 'E70': 1, 'E71': 1, 'E72': 1, 'E73': 1, 'E74': 1, 'E75': 1, 'E76': 1, 'E77': 1, 'E78': 1, 'E79': 1, 'E80': 1, 'E81': 1, 'E82': 1, 'E83': 1, 'E84': 1, 'E85': 1, 'E86': 1, 'E87': 1, 'E88': 1, 'E89': 1, 'E90': 1, 'E91': 1, 'E92': 1, 'E93': 1, 'E94': 1, 'E95': 1, 'E96': 1, 'E97': 1, 'refd': 1
}

collect_fields = {
    'type' : 1,
#    'flds' : 1, # fields, 
    'chan' : 1,

    'csts' : 1, # enum constants, list 
    'srcp' : 1, # source file
    'name' : 1, # name of item
    'retn' : 1,
    'ptd'  : 1,
    'valu' : 1, # list value for constants, 
    'value' :1,
#    'scpe' : 1,
    'elts' : 1,
    'prms' : 1, # paramtere
    'args' : 1,
    'argt' : 1,
    'refd' : 1,
    '_string' : 1, # string identifer

    'purp' : 1,
}

# each of these fields creates a field in the holder of them
collect_reverse = {
    'scpe' : {
        "result_decl" : "result", # only one...
        "const_decl" : "enums", # the constants of an enums
        "parm_decl" : "params",
        "field_decl" : "flds",
        "type_decl" : "types",
        "var_decl" : "vars",
        "function_decl" : "funcs",
        "label_decl" : "labels"
    }
}
reverse_fields = {}

collected = {}
for f in collect_fields:
    collected[f] = {}

    
for f in collect_reverse:
    # renaming the fields based on type
    for t in collect_reverse[f]:
        fn2 = collect_reverse[f][t]
        reverse_fields[fn2] = t
        collected[fn2] = {}



# read in the file and copy the data and create the first type layer
with open("../linux_clean_formatted_compact.json") as fi:
    for li in fi:
        row = json.loads(li)
        type_name = row[type_field]
        _id = row[identifier_field]
        usage[_id] += 1
        # save the row for second pass
        data[_id] = dict(row)

        # for f in row:
        #     if f not in collect_fields:
        #         if f not in collect_reverse:
        #             fields[f] =1
        if opt_collect_normal:
            for f in collect_fields:
                if f in row:
                    v = row[f]
                    collected[f][_id] = row[f]
                    usage[v] += 1

        # now reverse
        for f in collect_reverse:
            if f in row:

                if type_name not in collect_reverse[f]:
                    target_field = "rev_"+ type_name
                    collect_reverse[f][t] = target_field
                    if target_field not in collected:
                        collected[target_field] = {}
                else:
                    target_field = collect_reverse[f][type_name]

                v = row[f]
                usage[v] += 1
                if v in collected[target_field]:
                    collected[target_field][v].append( _id)
                else:
                    collected[target_field][v] = [ _id ]

    #pprint.pprint(collected)

counter=collections.Counter()

def generate_ids():
    eval_order = [
        'type',
    ]
    for fieldname in eval_order:
         path = [ fieldname ]
         for _id in collected[fieldname]:
             #         if data[_id]["_type"]== "type_decl":
             #             # now check the type
             #             _type = data[_id]["type"]
             #             if data[_type]["_type"]== "enumeral_type":
             yield (fieldname,_id)
                    
# field_order_array = [
#     ('csts', 'chan', 135 ),
#     ('csts', 'valu', 139),
#     ('elts', 'elts', 3 ),
#     ('elts', 'flds', 947 ),
#     ('elts', 'name', 221 ),
#     ('elts', 'ptd', 12 ),
# #    ('elts', 'scpe_rev', 25 ),
# #    ('flds', 'name', 612 ),
# #    ('flds', 'srcp', 629 ),
# #    ('flds', 'type', 629 ),
# #    ('flds', 'chan', 629 ),
#     # list nodes
#     ('chan', 'purp', 1 ),
#     ('chan', 'valu', 1 ), 
# #    ('name', 'name', 501 ),
# #    ('name', 'srcp', 560 ),
# #    ('name', 'type', 839 ),
# #    ('name', '_string', 1 ),    
#     ('ptd', 'csts', 2),
#     ('ptd', 'elts', 77),
# #    ('ptd', 'flds', 318),
#     ('ptd', 'name', 473),
#     ('ptd', 'ptd', 54),
#     ('ptd', 'retn', 406),
# #    ('ptd', 'scpe_rev', 187),
#     ('retn', 'csts', 13 ),
# #    ('retn', 'flds', 4 ),
#     ('retn', 'name', 1489 ),
#     ('retn', 'ptd', 352 ),
# #    ('scpe_rev', 'name', 582 ),
# #    ('scpe_rev', 'srcp', 924 ),
# #    ('scpe_rev', 'type', 933 ),
#     ('type', 'csts', 1607 ),
#     ('type', 'elts', 561),
#     ('type', 'flds', 2254),
#     ('type', 'name', 15245),
#     ('type', 'ptd', 5571),
#     ('type', 'retn', 4080 ),
#     ('type', 'type', 1 ),    
#     ('valu', 'csts', 34 ),
# #    ('valu', 'flds', 5 ),
#     ('valu', 'name', 1543 ),
#     ('valu', 'ptd', 2651 ),
#     ('valu', 'type', 1402 ),
#     ('valu', 'value', 1402 ),
#     ('value', 'chan', 31 ),
#     # ('value', 'csts', 1 ),
#     # ('value', 'elts', 5 ),
#     # ('value', 'flds', 13 ),
#     # ('value', 'name', 359 ),
#     # ('value', 'ptd', 8 ),
#     # ('value', 'retn', 15 ),
#     # ('value', 'scpe_rev', 15 ),
#     # ('value', 'srcp', 156 ),
#     # ('value', 'type', 398 ),
#     # ('value', 'valu', 32 ),
#     # ('value', 'value', 105 ),
# # type result
# # type enums
# # type params
# # type types
# # type vars
# # type funcs
# # type labels
# #     elts result
# #     elts enums
# #     elts params
# #     elts flds
# # elts types
# # elts vars
# # elts funcs
# # elts labels    
# # ptd result
# # ptd enums
# # ptd params
# # ptd flds
# # ptd types
# # ptd vars
# # ptd funcs
# # ptd labels    
# # retn result
# # retn enums
# # retn params
# # retn flds
# # retn types
# # retn vars
# # retn funcs
# # retn labels    
# # csts result
# # csts enums
# # csts params
# # csts flds
# # csts types
# # csts vars
# # csts funcs
# # csts labels    
# # valu result
# # valu enums
# # valu params
# # valu flds
# # valu types
# # valu vars
# # valu funcs
# # valu labels
# # value result
# # value enums
# # value params
# # value flds
# # value types
# # value vars
# # value funcs
# # value labels
# # chan result
# # chan enums
# # chan params
# # chan flds
# # chan types
# # chan vars
# # chan funcs
# # chan labels
# #    ' funcs result
# # funcs enums
# # funcs params
# # funcs flds
# # funcs types
# # funcs vars
# # funcs funcs
# # funcs labels
# ]
# field_order = { n[0]: {} for n in field_order_array }

field_order = {
    'flds' : { 'type': 629 },
    
    'chan': {'purp': 0, 'valu': 0},

    'csts': {'chan': 0, 'valu': 0},

    'elts': {'elts': 0, 'flds': 947, 'name': 0, 'ptd': 0},

    'funcs': {'labels': 802122,
              'params': 802374,
              'result': 802374,
              'types': 802354,
              'vars': 802374},

    'ptd': {'csts': 0, 'elts': 0, 'flds': 6376, 'name': 0, 'ptd': 0, 'retn': 0},

    'retn': {'csts': 0, 'name': 0, 'ptd': 0},
    
    'type': {'csts': 0,
             'elts': 0,
             'flds': 131031,
             'labels': 129141,
             'name': 0,
             'params': 130215,
             'ptd': 0,
             'result': 130215,
             'retn': 0,
             'type': 0,
             'types': 126684,
             'vars': 126684},

    'valu': {
        'csts': 0, 'name': 0, 'ptd': 0, 'type': 0, 'value': 0
    },
    
    'value': {
        'chan': 0,
        'enums': 50332,
        'flds': 50355,
        'funcs': 50332,
        'types': 50332,
        'vars': 50332
    }
}
 
# for n in field_order_array :
#     f1 = n[0]
#     f2 = n[1]
#     field_order[f1][f2]=0

    
def my_lookup_fields(field):
    # given a fieldname return what fields we should look for
    if field in field_order:
        for x in field_order[field]:
            yield x
        #else:
        #print("No next field for " + field, file=sys.stderr)

def chain(item, field, child):
    #print(child)
    item[field].append(child)

def myreduce2(item):
    # simplify nodes

    if item['st_field2'][-2:] == ['csts', 'chan']:
        if '__purp' in item:
            if '__valu' in item:
                item = { item['__purp']:item['__valu'] }
                #print(item)
            else:
                #print(item)
                item = { item['__purp']: "auto"}
        else:
            #print(item)
            item = { item['__valu'] : item['__valu']}
        print(item)
    elif item['st_field2'][-1] == 'csts':
        #print(item)
        pass
    #elif item['st_field2'][-1:] == ['csts']:
    #    print(item)

    return item

def doset(item, field, child):
    #print("resolve",item,field,child)
    fname = "__" + field
    
    if field in reverse_fields:
        if fname not in item :        
            item[fname] = [ child ] 
        else:
            item[fname].append( child)
    else:
        item[fname] = child
            
    return item


def myreduce(item):
    # simplify nodes
    #if item['field'] == 'purp':
    if item['st_field2'][-3:] == ['csts', 'chan', 'purp']:
        item = item['_string']
        #print(item['st_field2'])
    elif item['st_field2'][-3:] == ['csts', 'chan', 'valu']:
        item = item['from']
    # elif item['st_field2'][-2:] == ['csts', 'chan']:
    #     print(item)
    #     #item = { item['__purp'] : item['__valu'] }
    #     #print(item['st_field2'])
    #     pass
    # elif item['st_field2'][-1] == ['csts']:
    #     print(item)
    #     #item = { item['__purp'] : item['__valu'] }
    #     #print(item['st_field2'])
    #     pass
    return item

def process_graph(start_gen, lookup_fields):

    
    finished = [] # the items we have finished with
    

    for (fieldname,_id) in start_gen(): # generate the starting pairs

        queue = [  ] # the items to visit
        seen = {} # quick lookup on seen items
        root = {
            'started': None ,
            'st_field2' : ["root"],
        }
        root2 = {'started': root ,
                       'field':fieldname,
                       'from':_id ,
                       'st_field2' : [],
                       'resolve' : doset
        }
        
        # queue the starting point
        queue.append (root2)
        #print("starting with",_id)
        seen[_id]=1
        
        while len(queue ) > 0:
            #print(len(queue))
            item = queue.pop()
            nextid = item['from']
            field = item['field']

            if nextid in data:
                item["_type" ] = data[nextid]['_type']
                item["_data" ] = data[nextid]

            nameid = nextid
            for fieldname2 in ('name',):
                while nameid in collected[fieldname2]:
                    nameid = collected[fieldname2][nameid]
                    seen[nameid]=1
                    
                # resolved all names
                if nameid in collected['_string']:
                    item['_string'] = collected['_string'][nameid]
                
                    #if item['_type'] == "tree_list":
                #import pdb
                #pdb.set_trace()

            next_fields = list(lookup_fields(field))
            # for f2 in reverse_fields:
            #     if nextid in collected[f2]:
            #         next_fields.append(f2)
            #     if field in field_order:
            #         if f2 not in field_order[field]:
            #             if nextid in collected[f2]:
            #                 field_order[field][f2]=1
            #         else:
            #             field_order[field][f2]=field_order[field][f2]+1
            #     else:
            #         if nextid in collected[f2]:
            #             field_order[field]={ f2 : 1}
            #             #print(field,f2)

            for fieldname2 in next_fields:
                #if fieldname2 in ('_string',):
                    
                #print("field map", field, fieldname2)
                if nextid in collected[fieldname2]:
                    value2 = collected[fieldname2][nextid]
                    
                    if fieldname2 in ('chan',):
                        item[fieldname2]=[]
                        while value2 in collected[fieldname2]:
                            if value2 not in seen:
                                seen[value2]=1
                                
                                queue.append({
                                    'started': item,
                                    'from': value2,
                                    #'viaf': field,
                                    #'val': value2,
                                    'field': fieldname2,
                                    'resolve': chain,
                                })
                                # find the next value
                                #print("Chain", value2)
                                value2 = collected[fieldname2][value2]
                    else:
                        if isinstance(value2, list):
                            item[fieldname2]=[]
                            for v in value2:
                                if v not in seen:
                                    seen[v]=1
                                    queue.append({
                                        'started': item,
                                        'from': v,
                                        'field': fieldname2,
                                        'resolve' : doset,
                                    })
                        else:
                            if value2 not in seen:
                                seen[nextid]=1
                                #print("next item", nextid, fieldname2, value2)
                                queue.append({
                                    'started': item,
                                    #'viaf': field,
                                    'from': value2,
                                    #'val': value2,
                                    'field': fieldname2,
                                    'resolve' : doset,
                                })
            fn = item['resolve']
            st = item['started']
            del item['started']

            st_field2 = None
            if st:
                if 'st_field2' in st:
                    st_field2 = st['st_field2']
            
            del item['resolve']
            field = item['field']
            nextid = item['from']
            new_list = list(st_field2)
            new_list.append(field)
            item['st_field2'] = new_list

            if st:
                item = fn(st,field,item)
                if item:
                    if nextid in data:
                        item["_type" ] = data[nextid]['_type']
            #finished.append(myreduce(item))
        finished.append(root)


    return (finished)


def simple():
    yield ('type','23024')

def visit(x):
    ret = {}
    if isinstance(x,list):
        return [ visit(y) for y in x]
    
    for f in x :
        if f in ("_string",'_type'):
            ret[f] = x[f]
            
        elif f in ('chan',):
            ret[f] = visitchain(x[f])

        elif f.startswith("__"):
            ret[f] = visit(x[f])
    if len(ret.keys()) == 1:
        ret = ret[list(ret.keys())[0]]
    return ret

def visitchain(x):
    res = {}
    for y in x :
        if '__valu' in y:
            if '__purp' in y:
                res[ y['__purp']['_string'] ] = y['__valu']['_data']['value']
    return res

# def visit2(x):
#     ret = {}
#     for f in x :
#         if f in ("_string",'_type'):
#             ret[f] = x[f]
#         elif f in ('chan',):
#             ret[f] = visitchain(x[f])
#         elif f.startswith("__"):
#             ret[f] = visit(x[f])
#     return ret
def abstract(node, ret={}):
    if node is None :
        return "None"
    for field_name in node:        
        value = node[field_name]
        if field_name == '__csts':
            ret[field_name] = "CONSTANTS"

        elif isinstance(value,dict):
            ret[field_name] = abstract(value, {})
        elif isinstance(value,list):
            ret[field_name] = "list"
        elif field_name == '_type':
            ret['___type'] = value
        else:
            ret[field_name] = str(type(value))
            
    return ret
    
for x in process_graph(generate_ids, my_lookup_fields):
    y = visit(x)
    data = match_patterns(y)
    if data :
        #print(data)
        
        #print(json.dumps(abstract(data)))
        print(json.dumps(data))
    else:
        #print(json.dumps(abstract(y)))
        pass
    #pprint.pprint()
    #json.dump(visit(x),sys.stdout)
    #json.dump(x,sys.stdout)

