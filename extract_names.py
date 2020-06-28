# naming convention extractor
import re
import collections
import click

splitters = [
    '_____',
    '____',
    '___',
    '__',
    '_',
    ' ',
    '*',
    '.',
    "/"
]
def camel_to_snake(name):
  name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)

# camelcase
chars = collections.Counter()
@click.command()
@click.argument('fname')
def main(fname):
    with open(fname) as fi:
        for l in fi:
            l = l.strip().strip("\"")

            parts = { camel_to_snake(l) : 1}

            # split by 
            for s in splitters:
                for p in dict(parts):
                    for s2 in p.split(s):
                        if s2 not in parts:
                            parts[s2] =1
                            if p in parts:
                                del[parts[p]]

            for c in parts:
                chars[c]+=1

    for x in chars.most_common(20000):
        print(x)
            
if __name__ == '__main__':
    main()
