import pandas
import numpy as np
import random



googleCsv = pandas.read_csv('googleAdCategories/affinity_categories.csv')
fbCsv = pandas.read_csv('fbAdCategories/csv/fbInterestCategories.csv')

#print googleCsv.Category

matrix = pandas.DataFrame(index = fbCsv.category, columns = googleCsv.Category)

binaryList = [1]*10+[0]*90

def fillRandBinary(dataframe):
    for c in dataframe.columns:
        for i in dataframe.index:
            dataframe.set_value(i,c, int(random.choice(binaryList)))


matrix_ents = pandas.read_csv('matrix_ents.csv')



newIndex=[]
for i in matrix_ents['Unnamed: 0']:
    newIndex.append(i)

newColumns = []

for i in matrix_ents.columns[1:]:
   newColumns.append(i)


ndf = pandas.DataFrame(index = newIndex, columns = ['category']+newColumns)

new = pandas.DataFrame(columns = ['category']+newColumns)

#new.columns = ['category']+newColumns
new.fillna('columns')
new['category']=newIndex

new.to_csv('matrix_ents_modified.csv', sep=',', index=False)
mDf = pandas.read_csv('matrix_ents_modified.csv', index_col='category')

fillRandBinary(mDf)
mDf.astype(np.int32)




fbCols = []
for c in mDf.columns:
    if mDf[c]['/Entertainment']==1:
        print (True, c)
        fbCols.append(c)
print fbCols
print mDf.columns.tolist()

mDf.to_csv('matrix_ents_modified.csv', sep=',')


#print matrix.dtypes
fillRandBinary(matrix)
matrix.to_csv('matrix.csv', sep=',')



#mDf = pandas.read_csv('matrix.csv', index_col='category')
#print mDf.index
#print mDf

