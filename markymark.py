#!/usr/bin/python
#
# Copyright (c) 2009 James Bowes <jbowes@dangerouslyinc.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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

def _rainbowize(in_string):
    out_parts = []
    colors = (color_red, color_yellow, color_green, color_blue, color_magenta)
    i = 0
    for char in in_string:
        out_parts.append(colors[i % len(colors)] + char)
        i += 1

    return "".join(out_parts) + color_normal

def convert(in_string, return_to_normal=True):
    out_string = in_string
    for k, v in markup.items():
        out_string = out_string.replace("[%s]" % k, v)
        out_string = out_string.replace("[/%s]" % k, color_normal)

    parts = out_string.split("[rainbow]", 1)
    if len(parts) == 2:
        before = parts[0]
        parts = parts[1].split("[/rainbow]", 1)
        to_color = parts[0]
        after = parts[1]

        out_string = before + _rainbowize(to_color) + after

    if return_to_normal:
        out_string += color_normal

    return out_string

def _main():
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

if __name__ == "__main__":
    _main()
