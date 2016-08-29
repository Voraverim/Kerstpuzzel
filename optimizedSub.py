# -*- coding: utf-8 -*-
import collections
import unicodedata
# from difflib import SequenceMatcher

# Setting for extra output
verbose = True

# Lowercase alphabet a-z in list
alphabet = [chr(ord('a') + i) for i in range(26)]

# Get the type of a word, i.e. description of letter appearances
def getType(word):
    key = ''
    used = {' ': ' '}
    for letter in word:
        if not letter.isalpha():
            key += letter
            continue
        if letter not in used:
            used[letter] = alphabet[len(used)-1]
        key += used[letter]
    return key

# Load the list of words, a dictionary of the words is returned
def loadList():
    # First obtain a list of words from a text file
    unsortedWords = []
    with open('woordenlijstNLTotaal.txt', 'r') as inFile:
        unsortedWords = inFile.read().split('\n')
    # Then sort these into a dictionary based on their keys
    words = {}
    for word in unsortedWords:
        word = unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore').decode('utf-8').lower()
        key = getType(word)
        if key not in words:
            words[key] = []
        words[key].append(word)
    if verbose:
        print(sum(len(words[l]) for l in words), 'words loaded')
    return words

# Buffer the wordlist into a global variable, if it isn't already defined
if 'wordList' not in globals():
    wordList = loadList()

# Actual function that's useful
def getSubst(sentence):
    # Get all different words
    words = sentence.lower().split(' ')
    if verbose:
        print('List of words:', words)
        print('List of types:', [getType(word) for word in words])
    # Look up all the possibilities for each words
    possibilities = []
    for i, word in enumerate(words):
        possibilities.append((i, word, wordList[getType(word)]))
    if verbose:
        print('Possibilities for each word separately:', [len(x[2]) for x in possibilities])
    # Remove all combinations that are actually impossible
    possibilities.sort(key=lambda x: len(x[2]))
    # possibilities.sort(key=lambda x:  SequenceMatcher(None, x[1], ' '.join(word for word in words if word != x[1])).ratio())
    if verbose:
        print('Sorting order of words:', [x[0] for x in possibilities])
    beginningPossibilities = possibilities[0][2]
    for i in range(1, len(words)):
        newType = getType(' '.join(possibilities[j][1] for j in range(i+1)))
        newPossibilities = []
        for beginningPoss in beginningPossibilities:
            for poss in possibilities[i][2]:
                newPoss = beginningPoss + ' ' + poss
                if getType(newPoss) == newType:
                    newPossibilities.append(newPoss)
        beginningPossibilities = newPossibilities
    # Sort all the words back in place
    allPossibilities = []
    sortBy = [poss[0] for poss in possibilities]
    sortBy = [sortBy.index(i) for i in range(len(sortBy))]
    for beginningPoss in beginningPossibilities:
        beginningPossWords = beginningPoss.split(' ')
        allPossibilities.append(' '.join(beginningPossWords[i] for i in sortBy))
    if verbose:
        print('Possibilities for all words combined:', len(allPossibilities))
    # And we're done! We return it sorted for reading convenience
    return sorted(allPossibilities)

# Deleted code
    
    # # A list of lists? No, we clearly need nested dictionaries!
    # # Determine letter frequencies
    # freqs = ''
    # for letter, number in collections.Counter(''.join(words)).most_common():
    #     freqs += letter
    # # freqs = freqs[::-1]
    # # Nest it!
    # dictPossibilities = []
    # for i in range(len(possibilities)):
    #     nestedDict = {}
    #     for pos in possibilities[i]:
    #         tempDict = nestedDict;
    #         for letter in freqs:
    #             try:
    #                 l = words[i][pos.index(letter)]
    #             except ValueError:
    #                 l = ' '
    #             if l not in tempDict:
    #                 tempDict[l] = {}
    #             tempDict = tempDict[l]
    #     dictPossibilities.append(nestedDict)
    # # Remove all impossible combinations
    # def removeAllImpossibleCombinations(dictList):
    #     allTypes = ''
    #     for dic in dictList:
    #         allTypes += ''.join(key for key in dic)
    #     allTypes = allTypes.replace(' ', '')
    #     countTypes = collections.Counter(allTypes).most_common()
    #     maxOcc = countTypes[0][1]
    #     newTypes = ' '
    #     for letter, occ in countTypes:
    #         if occ < maxOcc:
    #             break
    #         newTypes += str(letter)
    #     for dic in dictList:
    #         for key in list(dic.keys()):
    #             if key not in newTypes:
    #                 del dic[key]
    # # incomplete
    # removeAllImpossibleCombinations(dictPossibilities)

    # if verbose:
    #     print('Possibilities for all words combined: a lot?')