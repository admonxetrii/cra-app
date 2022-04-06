import math


# split the sentences and count the repeated words
def wordCountMap(sentence):
    words = sentence
    wordCount = {}
    for word in words:
        if word in wordCount.keys():
            wordCount[word] = wordCount[word] + 1
        else:
            wordCount[word] = 1
    return (wordCount)


def addWordsToDisctionary(map, dict):
    for key in map:
        dict[key] = True


def wordMapToVector(map, dict):
    wordCountVector = []
    mapKey = 0;
    for key in dict:
        if key in map.keys():
            mapKey = map[key]
        else:
            mapKey = 0
        wordCountVector.append(mapKey)
    return wordCountVector


def dotProduct(vecA, vecB):
    product = 0
    for i in range(len(vecA)):
        product += vecA[i] * vecB[i]
    return product


def magnitude(vec):
    sum = 0
    for i in range(len(vec)):
        sum += vec[i] * vec[i]
    return math.sqrt(sum)


def cosine_similarity(vecA, vecB):
    return dotProduct(vecA, vecB) / (magnitude(vecA) * magnitude(vecB))


def descriptionCosineSimilarity(tagsA, tagsB):
    wordCountDescA = wordCountMap(tagsA)
    wordCountDescB = wordCountMap(tagsB)
    print(wordCountDescA, wordCountDescB)
    dict = {}
    addWordsToDisctionary(wordCountDescA, dict)
    addWordsToDisctionary(wordCountDescB, dict)
    vectorDescA = wordMapToVector(wordCountDescA, dict)
    vectorDescB = wordMapToVector(wordCountDescB, dict)
    return cosine_similarity(vectorDescA, vectorDescB)


