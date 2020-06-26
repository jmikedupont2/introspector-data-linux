#!/bin/bash
set +x

printf 'id\tvalue\ttype' > integer_csts.csv

jq -r '.nodes[]|select(._type=="integer_cst")| ._id + "\t" + .value + "\t" + .type' linux_clean.json >> integer_csts.csv
