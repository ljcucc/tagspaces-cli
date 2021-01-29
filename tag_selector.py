from pathlib import Path
from os import path
import os
import json
import terminal
from time import sleep
import datetime

selectedIndex = 0
tags = {}
selectedTags = {}
filepath = ""

def displayTag():
    global selectedIndex

    terminal.clearScreen()

    terminal.setTextColor(255,255,255)
    print("Add or remove tags with list below:")
    terminal.setTextColor(100,100,100)
    print("\n(switch using SPACE key, Done using ENTER key, \n\tJ and K for up and down like vim, \n\tD key for add new tag, \n\tQ for quit without save) \n")
    terminal.setTextColor(255,255,255)

    for (index, title) in enumerate(tags):
        print(" "*4+"(" + ("\u001b[7m" if selectedIndex == index else "\u001b[0m") + ("*" if title in selectedTags else " ") + "\u001b[0m) ", end="")
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
    
    if(len(tags.keys()) > 0):
        tags.update(data['tags'])
    else:
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
        result = addTag()
    elif(mode.lower() == "q"):
        terminal.clearScreen()
        confirm = input("WARNING: Are you sure you want to quit without save? (Y or yes) ")
        if(confirm.upper() == "Y" or confirm.upper() == "YES"):
            terminal.clearScreen()
            print("OK, Cancel it, won't do anything!")
            # sleep(1)
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
    elif(ord(mode) == 13):
        saveTagToFile()
        terminal.clearScreen()
        print("DONE! tags are written into .ts/ folder. check it out by typing `tags l`.")
        return


    if(selectedIndex < 0):
        selectedIndex = 0
    elif(selectedIndex >= len(tags.keys())):
        selectedIndex = len(tags.keys())-1


    displayTag()
    keyInput()

def getSpecialFormat():
    result = "T".join(str(datetime.datetime.now()).split(" "))
    result = result.split(".")
    result[1] = result[1][:3]
    result = ".".join(result)
    return result + "Z"

def addTag():
    terminal.clearScreen()
    print("# Add new tag:")
    terminal.setTextColor(100,100,100)
    print("WARNING: This aciton will not add any tag\n"+ (" "*9) +"into your global environment until you run `tags l -s`\n")
    terminal.setTextColor(255,255,255)
    name = input("name: ")
    color = input("color (default #fff, HEX only): ")
    color = color if color.strip() != "" else "ffffff"
    color = color if color[0] == "#" else "#"+color

    confirm = input("Sure you want this config? (Y for yes) ").upper()
    if confirm == "YES" or confirm == "Y":
        print("\nDone! adding...")
    else:
        print("\nTag won't add")
        sleep(1)
        terminal.clearScreen()
        return -1

    newTagData = {
       'type': 'sidecar',
       'title': name,
       'color': color,
       'textColor': 'white',
       'created_date': getSpecialFormat(),
       'modified_date': getSpecialFormat()
    } 

    tags.update({
        name: newTagData
    })

def updateTags():
    print("update tags...")

def runWithPath(received_filepath):
    global tags, selectedTags, filepath

    filepath = received_filepath

    print("edit tag with filepath...")
    getTagsFromPath(filepath)

    run()

def getTagsFromPath(filepath):

    data = {}

    filepath = path.dirname(filepath)+"/.ts/"+path.basename(filepath)+".json"
    print(filepath)

    if(not path.exists(filepath)):
        return {}

    with open(filepath, encoding='utf-8-sig') as jsonfile:
        data = json.load(jsonfile)
    
    fileTags = data['tags']
    
    for tag in fileTags:
        title = tag['title']
        
        if(not title in selectedTags):
            selectedTags.update({title:tag})
        
        if(not title in tags):
            tags.update({title:tag})

def saveTagToFile():
    global selectedTags, filepath

    tags = [selectedTags[title] for title in selectedTags]
    data = {
        'tags': tags,
        'appName': "TagSpaces"
    }

    ts_file = path.dirname(filepath) + "/.ts/" + path.basename(filepath) + ".json"

    if(not path.exists(path.dirname(filepath) + "/.ts/")):
        os.mkdir(path.dirname(filepath) + "/.ts/")

    with open(ts_file, mode="w", encoding='utf-8-sig') as jsonfile:
        json.dump(data, jsonfile)

def run():
    print("starting format...")

    readTags() # force read file
    displayTag() # first display

    keyInput() # looping

    # terminal.clearScreen()