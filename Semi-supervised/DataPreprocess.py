from Dataset.DataFilter import defaultFilters
from Dataset.DataFilter import Filter
from Dataset.DataFilter import processAclass
from Dataset.DataFilter import getPatternFilter

file1 = 'jojo.csv'
file2 =  'other.csv'

# load keys
f = open('jojo.txt')
k = f.read()
k = k.replace('\n','')
key = k.split('##')
keys = []
for i in key:
    if len(i) == 0:
        continue
    keys.append(i.split(' '))

