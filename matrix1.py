import pandas
import numpy as np
import random
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer


googleCsv = pandas.read_csv('googleAdCategories/affinity_categories.csv')
fbCsv = pandas.read_csv('fbAdCategories/csv/fbInterestCategories.csv')

#print googleCsv.Category

matrix = pandas.DataFrame(index = fbCsv.category, columns = googleCsv.Category)

binaryList = [1]*10+[0]*90

def fillRandBinary(dataframe):
    for c in dataframe.columns:
        for i in dataframe.index:
            dataframe.set_value(i,c, int(random.choice(binaryList)))



nltk.download('punkt') # if necessary...


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


'''
the form of input that we will have will be the following: 
fbAdCat = '/A/B&C/D E/F-G'
googleAdCat = '/A/B&C/D E/F-G'

need to split category by '/' then each item by space '&' and '-'

after splitting by slash and have a realtively cleaned up list
have a list to check if any of those splitters is in any of the items
'''


#code taken from http://stackoverflow.com/questions/28819272/python-how-to-calculate-the-cosine-similarity-of-two-word-lists



splitters = [' ']
toDelete = ['&','',' ']

def createSplittedList(selection):
    selection = selection.lower()
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
    #print ' '.join(new)
    return ' '.join(new)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


#print cosine_sim(createSplittedList('/Music Lovers/Folk & Traditional Music Enthusiasts'), createSplittedList('/Entertainment/Music/Jazz'))
#print cosine_sim('/Entertainment/Music/Jazz', '/Music Lovers/Jazz Enthusiasts')
#print cosine_sim('a little bird', 'a big dog barks')



matrixEnts = pandas.read_csv('matrix_ents_modified.csv', index_col='category')

def fillCosine(dataframe):
    for c in dataframe.columns:
        cList = createSplittedList(c)
        for i in dataframe.index:
            iList = createSplittedList(i)
            dataframe.set_value(i,c, cosine_sim(cList, iList))

fillCosine(matrixEnts)


matrixEnts.to_csv('matrix_ents_cosine.csv')
print matrixEnts



