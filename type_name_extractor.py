names = {
    'decl': 11526,
    'expr': 11246,
    'identifier_node': 8177,
    'tree_list': 5637,
    'type': 4363,
    'ref': 2438,
    'cst': 1360,
    'list': 470, # statement list
    'constructor': 49
}


def extract_name(name):

    parts = name.split("_")
    if name in names :
        return name

    part = parts[-1]
    if part in names:
        return part

