import terminal, os

selectedIndex = 0
cMode = ""
pwd = "../"
filelist = []
execRepeatTime = ""

def getchar():
	# Returns a single character from standard input
	ch = ''
	if os.name == 'nt': # how it works on windows
		import msvcrt
		ch = msvcrt.getch()
	else:
		import tty, termios, sys
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	if ord(ch) == 3: quit() # handle ctrl+C
	return ch

def move (y, x):
  print("\033[%d;%dH" % (y, x))

def getWidth():
  return os.get_terminal_size().columns

def getHeight():
  return os.get_terminal_size().lines

def clearScreen():
  from os import system, name
  if name == 'nt': 
    _ = system('cls') 
  else: 
    _ = system('clear')

def inputCommand():
  command = input(":")

  print("running command: "+ command)

def searchCommand():
  command = input(":(search) ")
  print("searching "+command)

def tagFileter():
  move(getHeight(),0)
  command = input(":(tag) ")
  clearScreen()
  move(getHeight(),0)
  print("searching tag...")
  
  # from time import sleep
  # sleep(3)

def getFileList(mypath):
  from os import listdir
  from os.path import isfile, join
  return [f for f in listdir(mypath) if isfile(join(mypath, f))]

def printFileList(mypath):
  global selectedIndex, cMode, filelist
  import glob

  filelist = paths = ["(Go back) ../"] + glob.glob(mypath)

  if selectedIndex >= len(paths):
    selectedIndex = len(paths) - 1

  for (index,path) in enumerate(paths):
    if(path == "(Go back) ../"):
      if(index == selectedIndex):
        print(bcolors.BG + path + (" " *(getWidth() - len(path))))
      else:
        print(bcolors.NORMAL + path + (" " *(getWidth() - len(path))))
      continue
    filename = " " + getFilename(path)
    if(folderMode() and isFile(path)):
      continue
    if(index == selectedIndex):
      print(bcolors.BG + filename + (" " *(getWidth() - len(filename))))
    else:
      print(bcolors.NORMAL + filename + (" " *(getWidth() - len(filename))))
  print(bcolors.NORMAL + (" "*getWidth()+'\n')*(getHeight() - len(paths) - 2))

  
  if(folderMode()):
    move(getHeight()-3, 0)
    print(bcolors.BG_BOLD + "--FOLDER MODE")
  
  move(getHeight()-2, 0)
  print(bcolors.NORMAL + getFullpath(mypath)[0])

def getFilename(mypath):
  import ntpath
  return ntpath.basename(mypath)

def isFolder(mypath):
  return os.path.isdir(mypath)

def isFile(mypath):
  return os.path.isfile(mypath)

def getFullpath(mypath):
  return os.path.abspath(mypath),

class bcolors:
  BG = '\033[0;30;47m'
  BG_BOLD = '\033[1;30;47m'
  NORMAL = '\033[0;37;40m'
  # HEADER = '\033[95m'
  # OKBLUE = '\033[94m'
  # OKCYAN = '\033[96m'
  # OKGREEN = '\033[92m'
  # WARNING = '\033[93m'
  # FAIL = '\033[91m'
  # ENDC = '\033[0m'
  BOLD = '\033[1m'
  # UNDERLINE = '\033[4m',

def updateSelectedIndex(inc):
  global selectedIndex
  selectedIndex += inc
  if(selectedIndex < 0):
    selectedIndex = 0

def folderMode():
  global cMode
  return "FOLDER-MODE" == cMode

def getRepeatTime():
  global execRepeatTime

  if(len(execRepeatTime) == 0):
    execRepeatTime = ""
    return 1

  result = int(execRepeatTime)
  execRepeatTime = ""
  return result


def isNaN(s):
    try: 
        int(s)
        return False
    except ValueError:
        return True

def main():
  global selectedIndex, cMode, pwd, execRepeatTime
  # print("(filelist)")
  clearScreen()

  printFileList(pwd + "/*")
  # print("height: " + str(getHeight()))
  # print("width: " + str(getWidth()))

  mode = getchar()

  if(mode == ":"):
    inputCommand()
  elif (mode == "/"):
    searchCommand()
  elif (mode == "#"):
    tagFileter()
  elif( mode == "k"):
    updateSelectedIndex(-1*getRepeatTime())
    main()
  elif (mode == "j"):
    updateSelectedIndex(1*getRepeatTime())
    main()
  elif (mode == "m"):
    if(cMode == "FOLDER-MODE"):
      cMode = ""
    else:
      cMode = "FOLDER-MODE"
    main()
  elif (mode == "M"):
    if(cMode == "NOTE-MODE"):
      cMode = ""
    else:
      cMode = "NOTE-MODE"
  elif (ord(mode) == 13): # [Enter] key
    selected = filelist[selectedIndex]
    if(selected == "(Go back) ../"):
      pwd = pwd+"/../"
      selectedIndex = 0
      main()
    if(isFolder(selected)):
      pwd = selected
      selectedIndex = 1
      main()
    else:
      print("opening...")
  elif (not isNaN(mode)):
    execRepeatTime += mode
    main()
  else:
    clearScreen()
    print(ord(mode))
    print("bye bye...")


def selectFile():
    print("listing file...")

    terminal.clearScreen()

    main()
    terminal.clearScreen()
    print()
    print("🔰 Try to using --file [path2file] to quickly add tags to file, more at `tags help add`.")
    print()

    return getFullpath(filelist[selectedIndex])[0]