import re
import math

content = open('./src/themes/quasar.ios.styl').read()
rem_regex = re.compile('(?P<n>[\d.]+) ?rem')

lines = content.split('\n')
px_lines = []
for line in lines:
    new_line = line
    for rem_number in rem_regex.findall(line):
        new_line = rem_regex.sub('%spx' % (float(rem_number)*16), new_line, count=1)
    px_lines.append(new_line)

px_regex = re.compile('(?P<n>[\d.]+) ?px')

res = []
for line in px_lines:
    new_line = line
    for px_number in px_regex.findall(line):
        new_line = px_regex.sub('%srem' %  round(float(px_number)/37.5, 3), new_line, count=1)
    res.append(new_line)

res = '\n'.join(res)

open('./src/themes/covert.ios.styl', 'w').write(res)