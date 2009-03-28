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

class MarkyMarkParseError(Exception):
    pass

curses.setupterm()

color_normal = curses.tigetstr('sgr0')
color_green = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_GREEN)
color_blue = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_BLUE)
color_magenta = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_MAGENTA)
color_red = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_RED)
color_white = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_WHITE)
color_yellow = curses.tparm(curses.tigetstr('setaf'), curses.COLOR_YELLOW)

bg_color_green = curses.tparm(curses.tigetstr('setab'), curses.COLOR_GREEN)
bg_color_blue = curses.tparm(curses.tigetstr('setab'), curses.COLOR_BLUE)
bg_color_magenta = curses.tparm(curses.tigetstr('setab'), curses.COLOR_MAGENTA)
bg_color_red = curses.tparm(curses.tigetstr('setab'), curses.COLOR_RED)
bg_color_white = curses.tparm(curses.tigetstr('setab'), curses.COLOR_WHITE)
bg_color_yellow = curses.tparm(curses.tigetstr('setab'), curses.COLOR_YELLOW)

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

bg_colors = {
    'bg:red' : bg_color_red,
    'bg:green' : bg_color_green,
    'bg:blue' : bg_color_blue,
    'bg:magenta' : bg_color_magenta,
    'bg:white' : bg_color_white,
    'bg:yellow' : bg_color_yellow,
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
    bg_color_stack = []
    attribute_stack = []
    rainbow_mark = 0

    out_string = ""
    for item in parts:
        omo = open.match(item)
        cmo = close.match(item)
        if omo:
            tag = omo.group(1)
            if colors.has_key(tag):
                out_string += colors[tag]
                color_stack.append(tag)
            elif bg_colors.has_key(tag):
                out_string += bg_colors[tag]
                bg_color_stack.append(tag)
            elif attributes.has_key(tag):
                out_string += attributes[tag]
                attribute_stack.append(tag)
            elif tag == 'rainbow':
                color_stack.append(tag)
            else:
                # unknown tag, just ignore it and put in output
                if len(color_stack) > 0 and color_stack[-1] == 'rainbow':
                    (rainbowed, rainbow_mark) = _rainbowize(item, rainbow_mark)
                    out_string += rainbowed
                else:
                    out_string += item
        elif cmo:
            tag = cmo.group(1)
            if len(color_stack) > 0 and color_stack[-1] == tag:
                color_stack.pop()
                if len(color_stack) == 0:
                    out_string += color_normal
                    for atr in attribute_stack:
                        out_string += attributes[atr]
                    if len(bg_color_stack) > 0:
                        out_string += bg_colors[bg_color_stack[-1]]
                elif color_stack[-1] != 'rainbow':
                    out_string += colors[color_stack[-1]]
            elif len(bg_color_stack) > 0 and bg_color_stack[-1] == tag:
                bg_color_stack.pop()
                if len(bg_color_stack) == 0:
                    out_string += color_normal
                    for atr in attribute_stack:
                        out_string += attributes[atr]
                    if len(color_stack) > 0 and color_stack[-1] != 'rainbow':
                        out_string += colors[color_stack[-1]]
                else:
                    out_string += bg_colors[bg_color_stack[-1]]
            elif len(attribute_stack) > 0 and \
                    attribute_stack[-1] == tag:
                attribute_stack.pop()
                # attributes are additive, so we need to remove this one then
                # reapply the others
                out_string += atr_normal
                for atr in attribute_stack:
                    out_string += attributes[atr]
                if len(color_stack) > 0 and color_stack[-1] != 'rainbow':
                    out_string += colors[color_stack[-1]]
                if len(bg_color_stack) > 0:
                    out_string += bg_colors[bg_color_stack[-1]]

            else:
                raise MarkyMarkParseError("Mismatched close tag '%s'" % tag)
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
