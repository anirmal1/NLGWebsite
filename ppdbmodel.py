#!usr/bin/env python3
import sys
sys.path.append('/homes/iws/anirmal/research/research-nlp-2018/')
import paraphraseAgePow as ppdb
import spacy
import gensim as gs
import kenlm
import pattern3.en as en

class PPDBModel():
  def __init__(self):
    self.nlp = spacy.load('en')
    # self.vectors = gs.models.KeyedVectors.load_word2vec_format('/homes/iws/anirmal/research/research-nlp-2018/retrofitted_vecs.txt', binary=False)
    self.vectors = gs.models.KeyedVectors.load_word2vec_format('/homes/iws/anirmal/NLGWebsite/weighted_retrofitted_vecs_word2vec.txt', binary=False)
    self.model = kenlm.Model('/tmp/anirmal/adventure-all.arpa')
    self.unknowns = []

  def getOutput(self, inputStr, dimension, change):
    # using spacy to get POS tags
    doc = self.nlp(inputStr)
    tags = [word.pos_ for word in doc]
    deps = [word.dep_ for word in doc]
    tokens = [token.text for token in doc]
    paraphrases = [[]]
    possible_words_per_token = []
    for i in range(len(tokens)):
      token = tokens[i]
      if tags[i] != 'VERB' or deps[i] == 'aux':
        for paraphrase in paraphrases:
          paraphrase.append(token)
        continue
      possible_words = None
      lem = en.lemma(token)
      if lem not in self.vectors.wv:
        self.unknowns.append((token, lem))
        continue
      val = ppdb.findParas(token, dim=dimension)
      if val is None:
        for paraphrase in paraphrases:
          paraphrase.append(token)
      else:
        print(val)
        paras = val.keys()
        similar_word = None
        values = val.values()
        '''
        if lem == 'travele':
          lem = 'travel'
        if lem == 'teethe':
          lem = 'teeth'
        if lem == 're-cover':
          lem = 'recover'
        '''
        if change == 'increase':
          max_val = max(values)
          if max_val > 0:
            possible_words = [para for para in paras if val[para] == max_val]
            '''
            orig_lems = [en.lemma(para) if en.lemma(para) != 'travele' else 'travel' for para in possible_words]
            orig_lems = [item if item != 'teethe' else 'teeth' for item in orig_lems]
            orig_lems = [item if item != 're-cover' else 'recover' for item in orig_lems]
            '''
            orig_lems = [en.lemma(para) for para in possible_words]
            lems = [item for item in orig_lems if self.nlp(item)[0].pos_ == 'VERB']
            lems = [item for item in lems if item in self.vectors.wv]
            if len(lems) > 0:
              similar_word = self.vectors.most_similar_to_given(lem, lems)
              similar_word = possible_words[orig_lems.index(similar_word)]
        else: # change == 'decrease'
          min_val = min(values)
          if min_val < 0:
            possible_words = [para for para in paras if val[para] == min_val]
            '''
            orig_lems = [en.lemma(para) if en.lemma(para) != 'travele' else 'travel' for para in possible_words]
            orig_lems = [item if item != 'teethe' else 'teeth' for item in orig_lems]
            orig_lems = [item if item != 're-cover' else 'recover' for item in orig_lems]
            '''
            orig_lems = [en.lemma(para) for para in possible_words]
            lems = [item for item in orig_lems if self.nlp(item)[0].pos_ == 'VERB']
            lems = [item for item in lems if item in self.vectors.wv]
            if len(lems) > 0:
              similar_word = self.vectors.most_similar_to_given(lem, lems)
              similar_word = possible_words[orig_lems.index(similar_word)]
        if similar_word == None:
          for paraphrase in paraphrases:
            paraphrase.append(token)
        else:
          # paraphrase.append(similar_word)
          new_paraphrases = []
          for paraphrase in paraphrases:
            for word in possible_words:
              p_copy = list(paraphrase)
              p_copy.append(word)
              new_paraphrases.append(p_copy)
          
          paraphrases = new_paraphrases
      if possible_words == None:
        possible_words_per_token.append('No paraphrases found for ' + token + '<br/>')
      else:
        possible_words_per_token.append('Paraphrases considered for ' + token + ': ' + str(possible_words) + '<br/>')
    paraphrase = None
    min_perplexity = None
    scores = dict()
    for p in paraphrases:
      perplexity = self.model.perplexity(" ".join(p))
      if min_perplexity == None or perplexity < min_perplexity:
        min_perplexity = perplexity
        paraphrase = p
      scores[" ".join(p)] = perplexity
    return " ".join(paraphrase), " ".join(possible_words_per_token), scores

