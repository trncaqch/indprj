
from gensim import models


model = models.Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)


