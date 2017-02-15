import pandas

matrix_w2v = pandas.read_csv('matrix_w2v.csv', index_col='category')

matrix_w2v.drop_duplicates()


print matrix_w2v
