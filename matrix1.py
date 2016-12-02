import pandas
import numpy as np

'''
This part converts fbAdCategories.json to .csv with index and category as headers
'''

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


fbCsv.category = sorted(fbCsv.category)
#print fbCsv

fbCsv.to_csv('fbAdCategories/fbInterestCategories.csv', sep = ',')

'''
'''

googleCsv = pandas.read_csv('googleAdCategories/affinity_categories.csv')


#print googleCsv.Category

matrix = pandas.DataFrame(index = fbCsv.category, columns = googleCsv.Category)
print matrix.columns


matrix.to_csv('matrix.csv', sep=',')

