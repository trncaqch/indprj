import pandas
import numpy as np


df = pandas.read_json('fbAdCategories/fbInterestCategories.json')
df = df['data']

pathLength = 0

fbCsv = pandas.DataFrame(data = None, columns = ["category"], index = range(329))




pos = 0

for i in df:
    row = ""
    for element in i['path']:
        row += "/" + element
    fbCsv["category"][pos] = row
    pos += 1


print sorted(fbCsv.category)


fbCsv.category = sorted(fbCsv.category)
print fbCsv

fbCsv.to_csv('fbAdCategories/fbInterestCategories.csv', sep = ',')
