from pathlib import Path
from os import path
import json
import terminal

selectedIndex = 0
tags = {}
selectedTags = {}

def displayTag():
    global selectedIndex

    print("Add or remove tags with list below:\n(switch using SPACE key, Done using ENTER key, D key for add new tag) \n")

    for (index, title) in enumerate(tags):
        print(" "*4+"(" + ("\u001b[7m" if selectedIndex == index else "\u001b[0m") + ("*" if title in selectedTags else " ") + "\u001b[0m)", end="")
        # print("\t("+ ("*" if selectedIndex == index else " ") +") " ,end="")
        terminal.printTag(tags[title])
        print()
    print()
    print("\033[%dA"% (5+ len(tags.keys())))

def readTags():
    global tags

    filepath = str(Path.home()) + "/.tagspaces.json"

    data = {
        'tags': {}
    }

    if(path.exists(filepath)):
        with open(filepath) as jsonfile:
            data = json.load(jsonfile)
    
    tags = data['tags']

def keyInput():
    global selectedIndex, selectedTags

    lastSelectedIndex = selectedIndex

    mode = terminal.getchar()

    if(mode == "j"):
        selectedIndex += 1
    elif(mode == "k"):
        selectedIndex -= 1
    elif(ord(mode) == 32):
        print(list(tags.keys()))
        title = list(tags.keys())[selectedIndex]
        if(not title in selectedTags):
            selectedTags.update({
                title: tags[title]
            })
        else:
            selectedTags.pop(title)
        print("\033[1A",end="")

    if(selectedIndex < 0):
        selectedIndex = 0
    elif(selectedIndex >= len(tags.keys())):
        selectedIndex = len(tags.keys())-1


    displayTag()
    keyInput()

def run():

    readTags() # force read file
    displayTag() # first display

    keyInput() # looping

    terminal.clearScreen()