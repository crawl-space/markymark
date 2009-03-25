#!/usr/bin/python

import curses

curses.setupterm()

color_normal = curses.tigetstr('sgr0')
color_green = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_GREEN)
color_blue = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_BLUE)
color_magenta = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_MAGENTA)
color_red = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_RED)
color_white = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_WHITE)
color_yellow = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_YELLOW)

bold = curses.tparm(curses.tigetstr('bold'), curses.A_BOLD)
underline = curses.tparm(curses.tigetstr('smul'), curses.A_UNDERLINE)
blink = curses.tparm(curses.tigetstr('blink'), curses.A_BLINK)

markup = {
    'red' : color_red,
    'green' : color_green,
    'blue' : color_blue,
    'magenta' : color_magenta,
    'white' : color_white,
    'yellow' : color_yellow,

    'b' : bold,
    'u' : underline,
    'blink' : blink,
} 


def convert(in_string, return_to_normal=True):
    out_string = in_string
    for k, v in markup.items():
        out_string = out_string.replace("[%s]" % k, v)
        out_string = out_string.replace("[/%s]" % k, color_normal)

    if return_to_normal:
        out_string += color_normal

    return out_string

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print "Usage: %s [--funky] [--bunch] TEXT" % sys.argv[0]
            sys.exit(0)
        elif sys.argv[1] in ["--funky", "--bunch"]:
            print "TODO: implement me"
            sys.exit(0)
        print convert(" ".join(sys.argv[1:]))
    else:
        for line in sys.stdin:
            sys.stdout.write(convert(line))