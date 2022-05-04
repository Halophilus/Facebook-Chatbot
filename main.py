import random
import json
import flatdict
import os
import sys

name = input("Enter your name: ")

def discoverFiles(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root,name))
    s = []
    for paths in r:
        if paths.endswith('.json'):
            s.append(paths)
    return s


def pullMessages(paths):
    messageList = []
    for file in paths:
        with open(file, 'r') as f:
            messages = json.load(f)
            rawMessages = messages['messages']
            for i in rawMessages:
                if i['sender_name'] == name and 'content' in i:
                    messageList.append(i['content'])
    return messageList

def removeAlert(messy):
    y = []
    for content in messy:
      if isBlacklisted(content):
          y.append(content)
    return y

def isBlacklisted(content):
    blacklist = ['You sent a','You voted for','You started a video','You set the ','You scored','You responded ','You named','You left ','You joined ','You invited ','You changed the','You called']
    for figs in blacklist:
        if content.startswith(figs):
            return False
    return True

def parseComments(dir):
    with open(dir, 'r') as e:
        comments = json.load(e)
        rawComments = comments['comments']
        flat_list = []
        for elements in rawComments:
            if 'data' in elements:
                elementsData = elements['data']
                for i in elementsData:
                    if 'comment' in i:
                        flatComment = i['comment']
                        if 'comment' in flatComment:
                            flat_list.append(flatComment['comment']) 
        return flat_list


def parseStatuses(dir):
    with open(dir,'r') as f:
        rawPosts = json.load(f)
        flat_list = []
        for elements in rawPosts:
            if 'data' in elements:
                elementsData = elements['data']
                for i in elementsData:
                    if 'post' in i:
                        flat_list.append(i['post'])
    return flat_list

if __name__ == '__main__':
    megaList = []
    comments = parseComments('comments/comments.json')
    messages = removeAlert(pullMessages(discoverFiles('messages/inbox')))
    statuses = parseStatuses('posts/your_posts_1.json')
    megaList.append(comments)
    megaList.append(messages)
    megaList.append(statuses)
    print(megaList)

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
   
