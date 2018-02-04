#!usr/bin/env python3
import sys
sys.path.append('/homes/iws/anirmal/research/research-nlp-2018/')
import paraphraseAgePow as ppdb
#from gensim.models.KeyedVectors import KeyedVectors
# import gensim as gs

'''
TODO 
- add slider to choose for increased or decreased power or agency
- add pos tagging (or something else) to better identify verbs (could also help identify subject and theme)
- connect site to server running on attu
'''

class PPDBModel():
  # def __init__(self):
  # self.vectors = gs.models.KeyedVectors.load_word2vec_format('/homes/iws/anirmal/research/research-nlp-2018/retrofitted_vecs.txt', binary=False)

  def getOutput(self, inputStr, dimension, change):
    tokens = inputStr.split()
    paraphrase = []
    for token in tokens:
      val = ppdb.findParas(token, dim=dimension)
      if val is None:
        paraphrase.append(token)
      else:
        print(val)
        paras = list(val.keys())
        similar_word = None
        if change == 'increase':
          max = -1
          for para in paras:
            if float(val[para]) > max:
              similar_word = para
        else:
          min = 1
          for para in paras:
            if float(val[para]) < min:
              similar_word = para

        if similar_word == None:
          paraphrase.append(token)
        else:
          # most_similar = self.vectors.most_similar_to_given(token, similar_words)
          paraphrase.append(similar_word)
    return " ".join(paraphrase)

