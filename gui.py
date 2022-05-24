from tempfile import tempdir
import tkinter
from tkinter import ttk, filedialog, IntVar, END
from tkinter.scrolledtext import ScrolledText
from main import *

root = tkinter.Tk()
root.title("Facebookinator")
frame = ttk.Frame(root, padding = 10)
frame.grid()
checkVar = tkinter.IntVar()
checkVar1 = tkinter.IntVar()
checkVar2 = tkinter.IntVar()
res = ""
comments = []
statuses = []
messages = []
name = ""

top = ttk.TopLevel(root, padding = 10)
top.grid()
top.title("Enter your name")
top.grab_set()
nameBox = tkinter.Text(top, height = 1, width = 30)
nameBox.grid(column = 0, row = 0)
enter = ttk.Button(top,)


checkVar = tkinter.IntVar()

topRow = ttk.Frame(frame, padding=0)
topRow.grid(column = 0, row = 0)

mainContent = ttk.Frame(frame, padding=0)
mainContent.grid(column = 0, row = 1)

generator = ttk.Frame(frame, padding=0)
generator.grid(column = 0, row = 2)

def setTextInput(text):
        tkinter.Text.insert(1.0, text)

dirBox = tkinter.Text(topRow , height = 1, width = 50)
dirBox.grid(column=1, row = 0)

def getDir():
    res = filedialog.askdirectory(title="Select a root directory for downloaded Facebook data")
    print(type(dirBox))
    dirBox.delete('1.0', END)
    dirBox.insert('1.0', res)

ttk.Button(topRow, text="Get Directory",command=getDir).grid(column=0,row=0)

contentsLabel = ttk.Label(mainContent, width = 15)
contentsLabel.grid(column = 1, row = 1)

statusLabel = ttk.Label(mainContent)
statusLabel.grid(column = 1, row = 1)
commentLabel = ttk.Label(mainContent)
commentLabel.grid(column = 1, row = 2)
messageLabel = ttk.Label(mainContent)
messageLabel.grid(column = 1, row = 3)

def messagesLabel():
    directory = 'messages/inbox'
    if dirBox.get(1.0, END) != '\n':
        directory = str.strip(dirBox.get(1.0, END)) + '/messages/inbox'
    try:
        messages = removeAlert(pullMessages(discoverFiles(directory), name))
    except FileNotFoundError:
        messages = []
    if tkinter.IntVar.get(checkVar2):
        if messages:
            statement = str(len(messages)) + ' found!'
            ttk.Label(mainContent, text = statement).grid(column = 1, row = 3)
            messageRandom["state"] = "enable"
        else:
            ttk.Label(mainContent, text = "None found!").grid(column = 1, row = 3)
    else:
        ttk.Label(mainContent, text = "                              ").grid(column = 1, row = 3)
        messageRandom["state"] = "disable"

def randMessage():
    directory = 'messages/inbox'
    if dirBox.get(1.0, END) != '\n':
        directory = str.strip(dirBox.get(1.0, END)) + '/messages/inbox'
    messages = removeAlert(pullMessages(discoverFiles(directory), name))
    randomMessage = random.choice(messages) + " | "
    text_area.insert(END, randomMessage)

def commentsLabel():
    directory = 'comments/comments.json'
    if dirBox.get(1.0, END) != '\n':
        directory = str.strip(dirBox.get(1.0, END)) + '/comments/comments.json'
    try:
        comments = parseComments(directory)
    except FileNotFoundError:
        comments = []
    if tkinter.IntVar.get(checkVar1):
        if comments:
            statement = str(len(comments)) + ' found!'
            ttk.Label(mainContent, text = statement).grid(column = 1, row = 2)
            commentRandom['state'] = 'enable'
        else:
            ttk.Label(mainContent, text = "None found!").grid(column = 1, row = 2)
    else:
        ttk.Label(mainContent, text = "                              ").grid(column = 1, row = 2)
        commentRandom['state'] = 'disable'

def randComment():
    directory = 'comments/comments.json'
    if dirBox.get(1.0, END) != '\n':
        directory = str.strip(dirBox.get(1.0, END)) + '/comments/comments.json'
    comments = parseComments(directory)
    randomComment = random.choice(comments) + " | "
    text_area.insert(END, randomComment)

def statusesLabel():
    directory = 'posts/your_posts_1.json'
    if dirBox.get(1.0, END) != '\n':
        directory = str.strip(dirBox.get(1.0, END)) + '/posts/your_posts_1.json'
    try: 
        statuses = parseStatuses(directory)
    except FileNotFoundError:
        statuses = []
    if tkinter.IntVar.get(checkVar):
        if statuses:
            statement = str(len(statuses)) + ' found!'
            ttk.Label(mainContent, text = statement).grid(column = 1, row = 1)
            statusRandom['state'] = 'enable'
        else:
            ttk.Label(mainContent, text = "None found!").grid(column = 1, row = 1)
    else:
        ttk.Label(mainContent, text = "                              ").grid(column = 1, row = 1)
        statusRandom['state'] = 'disable'

def randStatus():
    directory = 'posts/your_posts_1.json'
    if dirBox.get(1.0, END) != '\n':
        directory = str.strip(dirBox.get(1.0, END)) + '/posts/your_posts_1.json'
    statuses = parseStatuses(directory)
    randomStatus = random.choice(statuses) + " | "
    text_area.insert(END, randomStatus)


ttk.Checkbutton(mainContent, width = 15, variable = checkVar, text = 'Statuses:', command = statusesLabel).grid(column = 0, row = 1)
ttk.Checkbutton(mainContent, width = 15, variable = checkVar1, text = 'Comments:', command = commentsLabel).grid(column = 0, row = 2)
ttk.Checkbutton(mainContent, width = 15, variable = checkVar2, text = 'Messages:', command = messagesLabel).grid(column = 0, row = 3)


#ttk.Label(mainContent, text = contentScan).grid(column = 1, row = 1)

statusRandom = ttk.Button(mainContent,text="Pull Random", state= "disable", command = randStatus)
statusRandom.grid(column=2,row=1)
commentRandom = ttk.Button(mainContent,text="Pull Random", state= "disable", command = randComment)
commentRandom.grid(column=2,row=2)
messageRandom = ttk.Button(mainContent,text="Pull Random", state = "disable", command= randMessage)
messageRandom.grid(column=2,row=3)

def generate():
    megaList = []
    bigPhrase = ""
    if checkVar1.get() == 1:
        directory = 'comments/comments.json'
        if dirBox.get(1.0, END) != '\n':
            directory = str.strip(dirBox.get(1.0, END)) + '/comments/comments.json'
        try:
            comments = parseComments(directory)
        except FileNotFoundError:
            comments = []
        for i in comments:
            megaList.append(i)
            megaList.append(" | ")
    if checkVar.get() == 1:
        directory = 'posts/your_posts_1.json'
        if dirBox.get(1.0, END) != '\n':
            directory = str.strip(dirBox.get(1.0, END)) + '/posts/your_posts_1.json'
        try: 
            statuses = parseStatuses(directory)
        except FileNotFoundError:
            statuses = []
        for i in statuses:
            megaList.append(i)
            megaList.append(" | ")
    if checkVar2.get() == 1:
        directory = 'messages/inbox'
        if dirBox.get(1.0, END) != '\n':
            directory = str.strip(dirBox.get(1.0, END)) + '/messages/inbox'
        try:
            messages = removeAlert(pullMessages(discoverFiles(directory), name))
        except FileNotFoundError:
            messages = []
        for i in messages:
            megaList.append(i)
            megaList.append(" | ")
    if len(megaList) == 0:
        text_area.insert(END, " No content for generation! |")
    else:
        for phrases in megaList:
            bigPhrase+=phrases
        rndStatement = generateStatement(megaPhrasinator(bigPhrase))
        text_area.insert(END, rndStatement)



ttk.Button(generator, text="GENERATE", command = generate).grid(column = 0, row = 0, sticky = '')


        

text_area = tkinter.scrolledtext.ScrolledText(generator,  
                                      width = 40, 
                                      height = 10, 
                                      font = ("Times New Roman",
                                              15))
  
text_area.grid(column = 0, pady = 10, padx = 10)
root.mainloop()
