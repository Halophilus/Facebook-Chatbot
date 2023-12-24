import random
import json
import os

def readBlacklist():
    '''
    Reads a list of blacklisted words from a text file.
    Args:
        filePath (str): Path to the .txt file containing blacklisted words.
    Returns:
        set: A set of blacklisted words.
    '''
    with open('filter.txt', 'r') as file:
        blacklist = set(file.read().splitlines())
    return blacklist


def discoverFiles(dir):
    '''
    Discovers and lists all JSON files within a given directory.
    Args:
        dir (str): Directory path to search for JSON files.
    Returns:
        s (list): List of paths to JSON files found in the directory.
    '''
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    s = [paths for paths in r if paths.endswith('.json')]
    return s


def pullMessages(paths, nom):
    '''
    Extracts messages from JSON files where the sender matches the specified name.
    Args:
        paths (list): List of JSON file paths.
        nom (str): Name of the sender whose messages are to be extracted.
    Returns:
        messageList (list): List of messages sent by the specified sender.
    '''
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
    '''
    Filters out messages that are system alerts or not original content.
    Args:
        messy (list): List of messages to be filtered.
    Returns:
        list: Filtered list of messages with alerts removed.
    '''
    return [content for content in messy if isBlacklisted(content)]

def isBlacklisted(content):
    '''
    Determines if a message is a system alert or not.
    Args:
        content (str): Message content to be checked.
    Returns:
        bool: True if the content is not a system alert, False otherwise.
    '''
    blacklist = ['You sent a','You voted for','You started a video',
                 'You set the ','You scored','You responded ','You named',
                 'You left ','You joined ','You invited ','You changed the',
                 'You called']
    return not any(content.startswith(figs) for figs in blacklist)

class Comment:
    '''
    Class representing a Comment for easier handling and processing.
    '''
    def __init__(self, content):
        self.content = content

def parseComments(dir):
    '''
    Parses comments from a JSON file.
    Args:
        dir (str): Path to the JSON file containing comments.
    Returns:
        flat_list (list): List of comments extracted from the file.
    '''
    with open(dir, 'r') as e:
        comments = json.load(e)
        rawComments = comments['comments']
        flat_list = []
        for elements in rawComments:
            if 'data' in elements:
                for i in elements['data']:
                    if 'comment' in i and 'comment' in i['comment']:
                        flat_list.append(i['comment']['comment'])
        return flat_list

def parseStatuses(dir):
    '''
    Parses statuses from a JSON file.
    Args:
        dir (str): Path to the JSON file containing statuses.
    Returns:
        flat_list (list): List of statuses extracted from the file.
    '''
    with open(dir, 'r') as f:
        rawPosts = json.load(f)
        flat_list = [i['post'] for elements in rawPosts if 'data' in elements for i in elements['data'] if 'post' in i]
    return flat_list

def megaPhrasinator(megaPhrase):
    '''
    Processes a large string and generates a word count dictionary for Markov model.
    Args:
        megaPhrase (str): String to be processed.
    Returns:
        wordCount (dict): Dictionary mapping each word to the subsequent word's frequency.
    '''
    # Preprocess the phrase for consistency
    megaPhrase = (megaPhrase.lower().replace(".", " .").replace(",", " ,")
                  .replace("!"," !").replace("?"," ?").replace("\n"," ")
                  .replace("_"," ").replace("/"," or ").replace('"',' ')
                  .replace('-',' '))

    words = megaPhrase.split(" ")
    wordCount = {}
    for i in range(len(words) - 1):
        firstWord, secondWord = words[i], words[i + 1]
        if firstWord not in wordCount:
            wordCount[firstWord] = {}
        frequencies = wordCount[firstWord]
        frequencies[secondWord] = frequencies.get(secondWord, 0) + 1
    return wordCount

def chooseNext(wordCounts, word):
    '''
    Chooses the next word in a Markov chain sequence.
    Args:
        wordCounts (dict): Dictionary of word count frequencies for Markov model.
        word (str): Current word to find the next word for.
    Returns:
        str: Next word in the sequence, chosen based on frequency.
    '''
    if word in wordCounts:
        guesses = wordCounts[word]
        hat = [key for key, value in guesses.items() for _ in range(value)]
        return random.choice(hat)
    else:
        return None

def generateStatement(wordCount):
    '''
    Generates a random statement based on the Markov model, and replaces blacklisted words afterward.
    Args:
        wordCount (dict): Dictionary of word count frequencies for Markov model.
        blacklist (set): A set of blacklisted words.
    Returns:
        statement (str): Randomly generated statement with blacklisted words replaced.
    '''
    startingWord = random.choice(list(wordCount))
    statement = startingWord
    while True:
        nextWord = chooseNext(wordCount, startingWord)
        if nextWord is None or nextWord == "|":
            break
        statement += " " + nextWord
        startingWord = nextWord

    # Replace blacklisted words in the generated statement
    statement_words = statement.split()
    replaced_statement = ' '.join('[CENSORED]' if word in readBlacklist() else word for word in statement_words)

    return replaced_statement



# Example usage
# dir = 'path/to/facebook/data'
# all_paths = discoverFiles(dir)
# all_messages = pullMessages(all_paths, 'Your Name')
# clean_messages = removeAlert(all_messages)
# word_counts = megaPhrasinator(' '.join(clean_messages))
# print(generateStatement(word_counts))
