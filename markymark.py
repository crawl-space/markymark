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
import re

curses.setupterm()

color_normal = curses.tigetstr('sgr0')
color_green = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_GREEN)
color_blue = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_BLUE)
color_magenta = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_MAGENTA)
color_red = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_RED)
color_white = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_WHITE)
color_yellow = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_YELLOW)

# XXX these can be additive
atr_bold = curses.tparm(curses.tigetstr('bold'), curses.A_BOLD)
atr_underline = curses.tparm(curses.tigetstr('smul'), curses.A_UNDERLINE)
atr_blink = curses.tparm(curses.tigetstr('blink'), curses.A_BLINK)
atr_normal = curses.tparm(curses.tigetstr('sgr0'), curses.A_NORMAL)

colors = {
    'red' : color_red,
    'green' : color_green,
    'blue' : color_blue,
    'magenta' : color_magenta,
    'white' : color_white,
    'yellow' : color_yellow,
}

attributes = {
    'b' : atr_bold,
    'u' : atr_underline,
    'blink' : atr_blink,
} 

def _rainbowize(in_string, i):
    out_parts = []
    colors = (color_red, color_yellow, color_green, color_blue, color_magenta)
    for char in in_string:
        out_parts.append(colors[i % len(colors)] + char)
        i += 1

    return ("".join(out_parts), i)

def convert(in_string, return_to_normal=True):
    parts = re.split(r'(\[.*?\])', in_string)
    open = re.compile('\[([^/].*?)\]')
    close = re.compile('\[/(.*?)\]')

    color_stack = []
    attribute_stack = []
    rainbow_mark = 0

    out_string = ""
    for item in parts:
        omo = open.match(item)
        cmo = close.match(item)
        if omo:
            if colors.has_key(omo.group(1)):
                out_string += colors[omo.group(1)]
                color_stack.append(omo.group(1))
            elif attributes.has_key(omo.group(1)):
                out_string += attributes[omo.group(1)]
                attribute_stack.append(omo.group(1))
            elif omo.group(1) == 'rainbow':
                color_stack.append(omo.group(1))
            else:
                # unknown tag, just ignore it and put in output
                if len(color_stack) > 0 and color_stack[-1] == 'rainbow':
                    (rainbowed, rainbow_mark) = _rainbowize(item, rainbow_mark)
                    out_string += rainbowed
                else:
                    out_string += item
        elif cmo:
            if len(color_stack) > 0 and color_stack[-1] == cmo.group(1):
                color_stack.pop()
                if len(color_stack) == 0:
                    out_string += color_normal
                    for atr in attribute_stack:
                        out_string += attributes[atr]
                elif color_stack[-1] != 'rainbow':
                    out_string += colors[color_stack[-1]]
            elif len(attribute_stack) > 0 and \
                    attribute_stack[-1] == cmo.group(1):
                attribute_stack.pop()
                # attributes are additive, so we need to remove this one then
                # reapply the others
                out_string += atr_normal
                for atr in attribute_stack:
                    out_string += attributes[atr]
                if len(color_stack) > 0 and color_stack[-1] != 'rainbow':
                    out_string += colors[color_stack[-1]]
            else:
                # XXX error
                print "mismatched close tag"
        else:
            if len(color_stack) > 0 and color_stack[-1] == 'rainbow':
                (rainbowed, rainbow_mark) = _rainbowize(item, rainbow_mark)
                out_string += rainbowed
            else:
                out_string += item

    if return_to_normal:
        out_string += color_normal
        out_string += atr_normal

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
