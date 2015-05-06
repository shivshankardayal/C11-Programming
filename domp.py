#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys, os, fnmatch
from pygments import highlight
from pygments.lexers import *
from pygments.formatters import HtmlFormatter

def findReplace(directory, find, replace, filePattern):
        for path, dirs, files in os.walk(os.path.abspath(directory)):
                for filename in fnmatch.filter(files, filePattern):
                        filepath = os.path.join(path, filename)
                        with open(filepath) as f:
                                print filepath
                                s = f.read()
                                s = s.replace(find, replace)
                                s = s.replace("index.html", "")
                                soup = BeautifulSoup(s)

                                for i in soup.find_all("table", attrs={"summary": "Navigation header"}):
                                        i.contents[0].contents[0].clear()
                                        link = BeautifulSoup("<a href=\"../ix01.html\">Index</a>")
                                        i.contents[0].contents[0].insert(0, link)
                                        link = BeautifulSoup("<a href=\"../\">Home</a>")
                                        i.contents[1].contents[1].insert(0, link)
                                soup = BeautifulSoup(soup.renderContents())
                                for j in soup.findAll("table", attrs={"summary": "Navigation footer"}):
                                        link = BeautifulSoup("<a href=\"../ix01.html\">Index</a>")
                                        j.contents[0].contents[1].insert(0, link)
                                p = BeautifulSoup("Please see <a href=\"http://caniuse.com/#feat=mathml\">http://caniuse.com/#feat=mathml</a> if your browser supports MathML because certain sections of this book rely on MathML. If your browser does not support MathML please install Firefox from <a href=\"https://www.mozilla.org\">Mozilla</a> because AFAIK Firefox supports MathML.")
                                soup.body.insert(0, p)
                                soup = BeautifulSoup(soup.renderContents())
                                for i in soup.find_all("pre", "CommonLispLexer"):
                                        code = BeautifulSoup(highlight(i.string, CommonLispLexer(), HtmlFormatter()))
                                        i.string.replace_with(code)
                                soup = BeautifulSoup(soup.renderContents())
                                for i in soup.find_all("pre", "CLexer"):
                                        code = BeautifulSoup(highlight(i.string, CLexer(), HtmlFormatter()))
                                        i.string.replace_with(code)
                                soup = BeautifulSoup(soup.renderContents())
                                for i in soup.find_all("pre", "MakefileLexer"):
                                        code = BeautifulSoup(highlight(i.string, MakefileLexer(), HtmlFormatter()))
                                        i.string.replace_with(code)
                        with open(filepath, "w") as f:
                                f.write(soup.encode(formatter='html'))

findReplace("build/", "mml:", "", "index.html")
findReplace("build/", "mml:", "", "ix01.html")
