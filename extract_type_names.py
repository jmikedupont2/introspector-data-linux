import pprint

{
    'decl': 11526,
    'expr': 11246,
    'identifier_node': 8177,
    'tree_list': 5637,
    'type': 4363
    'ref': 2438,
    'cst': 1360,
    'list': 470, # statement list
    'constructor': 49,
}

basic = [ 'constructor',
          'expr',
          'type',
          'decl',
          'ref',
          'tree_list',
          "cst",
          'identifier_node'
          ]
names = { x:0  for x in basic }

with open("node_types.csv") as fi:
    for li in fi:
        li = li.strip()
        parts = li.split(" ")
        count = int(parts[0])
        name = parts[1]
        parts = name.split("_")
        if name in names :
            names[name] =  names[name]  + count
            continue
        #for c,part in enumerate(parts):
        part = parts[-1]
        if part not in names:
            names[part] =  0
            
        names[part] =  names[part]  + count
        

pprint.pprint(names)
