values = [1,3,3,1,1,5,2,2,1,4,4,2,3,1,1,3,10,1,1,1,4,4,4,8,8,6]

def getValue(c):
    return values[ord(c) - ord('a')]

def scrabble(w):
    x = 0
    for l in w:
        x += getValue(l)
    return x