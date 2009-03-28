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


from setuptools import setup

setup(name = "markymark",
      version = "0.3",
      description = "Make your console text funky!",
      author = "James Bowes",
      author_email = "jbowes@dangerouslyinc.com",
      url = "http://github.com/jbowes/markymark",
      platforms = ["any"],
      license = "MIT",
      keywords = ["cli", "console", "text", "color", "ANSI"],

      classifiers = [
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "Intended Audience :: Other Audience",
          "License :: OSI Approved :: MIT License",
          "Topic :: Software Development :: Libraries",
          "Topic :: Software Development :: User Interfaces",
          "Topic :: Text Processing :: Markup",
          "Topic :: Utilities",
      ],

      py_modules = ["markymark"],
      entry_points = {
          'console_scripts' : [
              'markymark = markymark:_main',
          ],
      }
)
