import os

def setTextColor(r,g,b):
    print("\x1b[38;5;%dm"% (rgb_to_xterm(r,g,b)), end="")

# reference from: https://stackoverflow.com/questions/11765623/convert-hex-to-closest-x11-color-number
def rgb_to_xterm(r, g, b):
    N = []
    for i, n in enumerate([47, 68, 40, 40, 40, 21]):
        N.extend([i]*n)

    mx = max(r, g, b)    
    mn = min(r, g, b)

    if (mx-mn)*(mx+mn) <= 6250:
        c = 24 - (252 - ((r+g+b) // 3)) // 10
        if 0 <= c <= 23:
            return 232 + c

    return 16 + 36*N[r] + 6*N[g] + N[b]

def hex_to_rgb(hx, hsl=False):
    import re
    if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(int(hx[i]*2, 16) / div if div else
                         int(hx[i]*2, 16) for i in (1, 2, 3))
        return tuple(int(hx[i:i+2], 16) / div if div else
                     int(hx[i:i+2], 16) for i in (1, 3, 5))
    raise ValueError(f'"{hx}" is not a valid HEX code.')

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

def printTag(tag):
    colorCode = tag['color'][:-2]
    rgbCode = hex_to_rgb(colorCode)

    setTextColor(rgbCode[0], rgbCode[1],rgbCode[2])
    print(tag['title'], end="")

    setTextColor(255,255,255)
    print(", ", end="")
    