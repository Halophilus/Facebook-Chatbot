import random

sample = open("data.txt", "r", errors="ignore")
data = sample.read()
sample.close()

data = (data
    .lower()
    .replace(".", " .")
    .replace(",", " ,")
    .replace("\n"," ")
)
words = data.split(" ")

wordCount = {}
wordsLength = len(words)
wordsRange = range(wordsLength - 1)

for i in wordsRange:
    firstWord = words[i]
    secondWord = words[i+1]
    if firstWord not in wordCount:
        wordCount[firstWord] = {}
    frequencies = wordCount[firstWord]
    if secondWord not in frequencies:
        frequencies[secondWord] = 1
    else:
        frequencies[secondWord] = frequencies[secondWord] + 1

def chooseNext(wordCounts, word):
    hat = []
    if word in wordCounts:
        guesses = wordCounts[word]
        for key,value in guesses.items():
            for _ in range(value):
                hat.append(key)
        return random.choice(hat)
    else:
        return None
    wordCounts[word]

def generateStatement(wordCount):
    startingWord = random.choice(list(wordCount))
    statement = startingWord
    while True:
        startingWord = chooseNext(wordCount, startingWord)
        if startingWord is None:
            break
        statement = statement + " " + startingWord
        if startingWord == ".":
            break
    return statement

for _ in range(1):
    print(generateStatement(wordCount))
   
   