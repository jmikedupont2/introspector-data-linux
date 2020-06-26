# introspector-data-linux
Introspector data repo from the linux kernel
This branch is for processing the perf tools

linux_clean_formatted.json contains clean data.

The data is put with one row on each line like this:
`jq . linux_clean_formatted.json  -c > linux_clean_formatted_compact.json `

if the _type is "integer_cst", extract the type and value,
try and associate the value to the type, and the type to the value.
See if we can extract information

```
echo "id\tvalue\ttype' > integer_csts.csv
jq '.nodes[]|select(._type=="integer_cst")|._id + "\t" .value + "\t" + .type' linux_clean.json  -r >> integer_csts.csv
```

The number of values
`cut -f 2 integer_csts.csv  | sort | uniq -c | sort -n`


```
jq '.nodes[]|select(._type=="integer_type")' linux_clean.json  | cut -d: -f1 | sort | uniq -c | sort -n
```

qualified integer type

31   "qual"

unqualified integer type

    251   "unql"
	
	named integer types

    270   "name"

bound max integer types 
358   "max"

bound min integer types 
359   "min"

All integer type

    360   "_id"
    360   "_type"
	
    360   "algn"
    360   "prec"
    360   "sign"
    360   "size"
	
	Extract the integer_type items referenced. 

```
jq '.nodes[]|select(._type=="integer_type")| select(.qual)|._id + "\t" .size + "\t" + .sign + "\t" + .prec + "\t" + .algn + "\t" + .min + "\t" + .max + "\t" + .name + "\t" + .unqual + "\t" + .qual    ' linux_clean.json  -r  > integer_type.csv
```

# feature preparation

`python3 prepare_features.py > expanded_data.json`

extract the most common keys like this :
`jq -r ".|keys" expanded_data.json | sort | uniq -c | sort -n > common_paths.txt`

see common_paths.txt for the top ones

`jq -r "._type" expanded_data.json | sort | uniq -c | sort -n > type_count.txt`

Extract the most common one:

`grep "\"_type\": \"identifier_node__stringstring_identifier_node__string_lenpythonint" expanded_data.json | sort -u > indentifiers.txt`
grep "\"_type\": \"identifier_node__stringstring_identifier_node__string_lenpythonint" expanded_data.json| jq ._string  -r | sort -u > names.txt
