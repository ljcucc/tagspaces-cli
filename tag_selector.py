from pathlib import Path
from os import path
import json
import terminal
from time import sleep

selectedIndex = 0
tags = {}
selectedTags = {}

def displayTag():
    global selectedIndex

    terminal.clearScreen()

    terminal.setTextColor(255,255,255)
    print("Add or remove tags with list below:")
    terminal.setTextColor(100,100,100)
    print("\n(switch using SPACE key, Done using ENTER key, \n\tD key for add new tag, \n\tQ for quit without save) \n")
    terminal.setTextColor(255,255,255)

    for (index, title) in enumerate(tags):
        print(" "*4+"(" + ("\u001b[7m" if selectedIndex == index else "\u001b[0m") + ("*" if title in selectedTags else " ") + "\u001b[0m)", end="")
        # print("\t("+ ("*" if selectedIndex == index else " ") +") " ,end="")
        terminal.printTag(tags[title])
        print()
    print()
    # print("\033[%dA"% (5+ len(tags.keys())))

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
    elif(mode == "d" or mode == "D"):
        addTag()
    elif(mode.lower() == "q"):
        terminal.clearScreen()
        confirm = input("WARNING: Are you sure you want to quit without save? (Y or yes) ")
        if(confirm.upper() == "Y" or confirm.upper() == "YES"):
            terminal.clearScreen()
            print("OK, Cancel it, won't do any change!")
            sleep(1)
            return
    elif(ord(mode) == 32):
        # print(list(tags.keys()))
        title = list(tags.keys())[selectedIndex]
        if(not title in selectedTags):
            selectedTags.update({
                title: tags[title]
            })
        else:
            selectedTags.pop(title)
        # print("\033[1A",end="")

    if(selectedIndex < 0):
        selectedIndex = 0
    elif(selectedIndex >= len(tags.keys())):
        selectedIndex = len(tags.keys())-1


    displayTag()
    keyInput()

def addTag():
    terminal.clearScreen()
    print("# Add new tag:")
    terminal.setTextColor(100,100,100)
    print("WARNING: This aciton will not add any tag\n"+ (" "*9) +"into your global environment until you run `tags l -s`\n")
    terminal.setTextColor(255,255,255)
    name = input("name: ")
    color = input("color (default #fff): ")

    confirm = input("Sure you want this config? (Y for yes) ").upper()
    if confirm == "YES" or confirm == "Y":
        print("\nDone! adding...")
    else:
        print("\nTag won't add")
    
    sleep(1)
        
    terminal.clearScreen()

def run():

    readTags() # force read file
    displayTag() # first display

    keyInput() # looping

    terminal.clearScreen()