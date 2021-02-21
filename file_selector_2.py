import urwid

# copy from http://urwid.org/tutorial/index.html

main = urwid.Padding(menu(u'Choose a file', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)

def run():
    global top
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
