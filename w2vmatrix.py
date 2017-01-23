import pandas

import string


import gensim
import numpy


model = gensim.models.Word2Vec.load_word2vec_format(
                      "../word2vec/wiki.en.bin.vector", binary=True)


googleCsv = pandas.read_csv('googleAdCategories/affinity_categories.csv')
fbCsv = pandas.read_csv('fbAdCategories/csv/fbInterestCategories.csv')

#print googleCsv.Category

matrix = pandas.DataFrame(index = fbCsv.category, columns = googleCsv.Category)


'''
the form of input that we will have will be the following: 
fbAdCat = '/A/B&C/D E/F-G'
googleAdCat = '/A/B&C/D E/F-G'

need to split category by '/' then each item by space '&' and '-'

after splitting by slash and have a realtively cleaned up list
have a list to check if any of those splitters is in any of the items
'''


#code taken from http://stackoverflow.com/questions/28819272/python-how-to-calculate-the-cosine-similarity-of-two-word-lists

#function to replace a list element
def replace_list_el(l, X, Y):
    for i,v in enumerate(l):
        if v == X:
            l.pop(i)
            l.insert(i, Y)



splitters = [' ']
toDelete = ['&','',' ',',',';','.']

def createSplittedList(selection):
    selection = selection.lower()
    selection = selection.replace('-',' ')
    selection = selection.replace(',','')
    new = selection.split('/')
    new.remove('')
    new2 = new[:]
    for i in new2:
        for spl in splitters:
            if spl in i:
                new.remove(i)
                new += i.split(spl)
    for term in toDelete:
        if term in new:
            new.remove(term)
    #return list item
    if 'e' in new:
        new.remove('e')
        replace_list_el(new,'books', 'ebooks')
    return new

#text1 and text2 are list items
def wiki_w2v_sim(text1, text2):
    sim = model.n_similarity(text1,text2)
    print sim
    return sim


matrixEnts = pandas.read_csv('matrix_ents_modified.csv', index_col='category')

def fillSimilarities(dataframe):
    for c in dataframe.columns:
        cList = createSplittedList(c)
        for i in dataframe.index:
            iList = createSplittedList(i)
            print (c,i)
            dataframe.set_value(i,c, wiki_w2v_sim(cList, iList))

fillSimilarities(matrixEnts)


matrixEnts.to_csv('matrix_ents_w2v.csv')
print matrixEnts



