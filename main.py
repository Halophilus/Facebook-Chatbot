import random
import json
import flatdict
import os
import sys



def discoverFiles(dir):
    # return [ os.path.join(root,name)
    #          for root, dirs, files in os.walk(dir)
    #          for name in files
    #          if name.endswith('.json') ]
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root,name))
    s = []
    for paths in r:
        if paths.endswith('.json'):
            s.append(paths)
    return s


def pullMessages(paths, nom):
    messageList = []
    for file in paths:
        with open(file, 'r') as f:
            messages = json.load(f)
            rawMessages = messages['messages']
            for i in rawMessages:
                if i['sender_name'] == nom and 'content' in i:
                    messageList.append(i['content'])
    return messageList

def removeAlert(messy):
    return [ content 
             for content in messy 
             if isBlacklisted(content) ]

def isBlacklisted(content):
    blacklist = ['You sent a','You voted for','You started a video','You set the ','You scored','You responded ','You named','You left ','You joined ','You invited ','You changed the','You called']
    for figs in blacklist:
        if content.startswith(figs):
            return False
    return True

class Comment:
    def __init__(self, content):
        self.content = content

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

def megaPhrasinator(megaPhrase):
    megaPhrase = (megaPhrase
            .lower()
            .replace(".", " .")
            .replace(",", " ,")
            .replace("!"," !")
            .replace("?"," ?")
            .replace("\n"," ")
            .replace("_"," ")
            .replace("/"," or ")
            .replace('"',' ')
            .replace('-',' ')
    )
    words = megaPhrase.split(" ")
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
    return wordCount


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


def generateStatement(wordCount):
    startingWord = random.choice(list(wordCount))
    statement = startingWord
    counter = 0
    while True:
        startingWord = chooseNext(wordCount, startingWord)
        if startingWord is None:
            break
        statement = statement + " " + startingWord
        if startingWord == "|":
            counter+=1
        if counter == 50:
            break
    return statement


        
   
