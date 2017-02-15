import pandas

matrix = pandas.read_csv('matrix.csv', index_col='category')

matrix[matrix.columns] = matrix[matrix.columns].astype(float)


matrix.to_csv('matrix.csv')
print matrix.head(10)