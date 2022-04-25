print("Hello world")

sample = open("data.txt", "r")
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

print(wordCount)


