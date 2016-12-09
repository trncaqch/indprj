import pandas
import numpy as np
import random





binaryList = [1]*10+[0]*90

def fillRandBinary(dataframe):
    for c in dataframe.columns:
        for i in dataframe.index:
            dataframe.set_value(i,c, int(random.choice(binaryList)))



mDf = pandas.read_csv('matrix_ents_modified.csv', index_col='category')

fillRandBinary(mDf)
mDf.astype(np.int32)



#Testing with selection being '/Entertainment'
fbCols = []
for c in mDf.columns:
    if mDf[c]['/Entertainment']==1:
        print (True, c)
        fbCols.append(c)
print fbCols
print mDf.columns.tolist()

mDf.to_csv('matrix_ents_modified.csv', sep=',')



matrix = pandas.DataFrame(index = fbCsv.category, columns = googleCsv.Category)
fillRandBinary(matrix)
matrix.to_csv('matrix.csv', sep=',')
