#!usr/bin/env python3
import sys
sys.path.append('/homes/iws/anirmal/research/research-nlp-2018/')
import paraphraseAgePow as ppdb

class PPDBModel():
  def getOutput(self, inputStr, dimension):
    tokens = inputStr.split()
    paraphrase = []
    for token in tokens:
      val = ppdb.findParas(token, dim=dimension)
      if val is None:
        paraphrase.append(token)
      else:
        print(val)
        paraphrase.append(list(val.keys())[0])
    return " ".join(paraphrase)

'''
  def getOutput(self, inputStr):
    initialVal = ppdb.findParas(inputStr)
    if initialVal is not None:
      return list(initialVal.keys())[0] #TODO check this type
    tokens = inputStr.split()
    options = []
    options.append([True])
    options.append([False])
    for i in range(1, len(tokens) - 1): # because 1 less place to split than number of tokens
      tempOptions = []
      for option in options:
        trueOp = list(option)
        falseOp = list(option)
        trueOp.append(True)
        falseOp.append(False)
        tempOptions.append(trueOp)
        tempOptions.append(falseOp)
      options.extend(tempOptions)

    for option in options:
      words = list(tokens)
      for i in range(len(option) - 1, 0, -1):
        if option[i] == True: # TODO
         words[i] = words[i] + " " + words[i + 1]
         del words[i + 1]
      print(words)
      paraphrase = []
      for word in words:
        val = ppdb.findParas(word)
        if val is None:
          continue
        paraphrase.append(list(val.keys())[0])
      if len(paraphrase) < len(words):
        continue
      return " ".join(paraphrase)

    return inputStr # if all else fails
'''
'''
	  tokens = inputStr.split()
    for token in tokens:
      values = ppdb.findParas(token)
    # TODO extract values
'''

