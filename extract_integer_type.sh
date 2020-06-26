
printf "id\tsize\tsign\tprec\talgn\tmin\tmax\tname\tunqual\tqual\n"  > integer_type.csv
jq '.nodes[]|select(._type=="integer_type")| ._id + "\t" + .size + "\t" + (.sign | tostring ) + "\t" + (.prec | tostring) + "\t" + (.algn | tostring) + "\t" + .min + "\t" + .max + "\t" + .name + "\t" + .unqual + "\t" + .qual    ' linux_clean.json  -r  >> integer_type.csv
