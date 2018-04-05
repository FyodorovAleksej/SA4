import pymorphy2
from sklearn.feature_extraction.text import CountVectorizer
import os
import numpy as np
import re

def f_tokenizer(s):
    words = re.split("[\\s,.!?()\\[\\]\"\'<>]", s)
    resultWords = []
    for word in words:
        morphem = morph.parse(word.replace('.',''))
        if len(morphem) > 0:
            wrd = morphem[0]
            if wrd.tag.POS not in ('NUMR','PREP','CONJ','PRCL','INTJ'):
                resultWords.append(wrd.normal_form)
    return resultWords

def joinTexts(paths):
    texts = []
    for path in paths:
        file = open(path)
        text = file.read()
        file.close()
        texts.append(text)
    return texts

def normal(list1, list2):
    LEN1 = len(list1)
    LEN2 = len(list2)
    if (LEN1 == LEN2):
        return np.array(list1) + np.array(list2)
    if (LEN1 > LEN2):
        adding = [0 for i in range(0, LEN1 - LEN2)]
        return np.array(list1) + np.array(list2 + adding)
    adding = [0 for i in range(0, LEN2 - LEN1)]
    return np.array(list1 + adding) + np.array(list2)

def saveDiction(name, words):
    file = open(os.getcwd() + "\\input\\" + str(name) + "Diction.txt", "w+")
    print(name + ":")
    for word in words[:-1]:
        if (word != ""):
            print(word)
            file.write(word + "\n")
    file.write(words[-0])
    file.close()

if __name__ == "__main__":
    morph = pymorphy2.MorphAnalyzer()
    #dictions = [os.getcwd() + "\\input\\diction" + str(i) + ".txt" for i in range(1, 5)]
    paths = [os.getcwd() + "\\text\\text-" + str(i) + ".txt" for i in range(1, 5)]
    gamePaths = [os.getcwd() + "\\text\\game-" + str(i) + ".txt" for i in range(1, 4)]
    greenPaths = [os.getcwd() + "\\text\\green-" + str(i) + ".txt" for i in range(1, 4)]
    itPaths = [os.getcwd() + "\\text\\it-" + str(i) + ".txt" for i in range(1, 4)]
    medPaths = [os.getcwd() + "\\text\\med-" + str(i) + ".txt" for i in range(1, 4)]

    MINBORDER = 10

    texts = {"green": joinTexts(greenPaths), "med": joinTexts(medPaths), "it": joinTexts(itPaths), "game": joinTexts(gamePaths)}
    kinds = ["green", "med", "it", "game"]

    dictions = {i: [] for i in kinds}
    vectorizer = CountVectorizer(tokenizer=f_tokenizer)
    vectors = {i: vectorizer.fit_transform(texts[i]).toarray().tolist() for i in kinds}
    for key in vectors.keys():
        sumVector = [0 for i in range(0, len(vectorizer.vocabulary_.items()))]
        for vector in vectors[key]:
            sumVector = normal(sumVector, vector).tolist()
        for item in vectorizer.vocabulary_.items():
            if (sumVector[item[1]] >= MINBORDER):
                dictions[key].append(item[0])
    for dictionName in dictions.keys():
        saveDiction(dictionName, dictions[dictionName])