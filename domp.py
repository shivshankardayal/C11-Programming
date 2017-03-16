#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys, os, fnmatch
from pygments import highlight
from pygments.lexers import *
from pygments.formatters import HtmlFormatter
from string import *
import multiprocessing

files_list = []

def findReplace(directory, find, replace, filePattern):
        global files_list
        for path, dirs, files in os.walk(os.path.abspath(directory)):
                for filename in fnmatch.filter(files, filePattern):
                        filepath = os.path.join(path, filename)
                        #print filepath
                        files_list.append(filepath)


def setup(files):
    jobs = []
    for i in range(len(files)):
        p = multiprocessing.Process(target=process, args=(files[i],))
        jobs.append(p)

        p.start()

def process(filepath):
    #print "in process"
    print(filepath)
    with open(filepath) as f:
            # print "opened " + filepath
            l = filepath.split('/')
            name = ''
            if(l[len(l) -2]) == 'build':
                name = l[len(l) - 1]
            s = f.read()
            #s = s.replace(find, replace)
            s = s.replace("index.html", "")
            soup = BeautifulSoup(s, "lxml")

            for i in soup.find_all("table", attrs={"summary": "Navigation header"}):
                    i.contents[0].contents[0].clear()
                    if name == "index.html":
                            link = BeautifulSoup("<a href=\"ix01.html\">Index</a>", "lxml")
                    elif name =="ix01.html":
                            link = BeautifulSoup("", "lxml")
                    else:
                            link = BeautifulSoup("<a href=\"../ix01.html\">Index</a>", "lxml")
                            i.contents[0].contents[0].insert(0, link)
                    if name == "index.html":
                            link = BeautifulSoup("", "lxml")
                    elif name == "ix01.html":
                            link = BeautifulSoup("<a href=\"index.html\">Table of Contents</a>", "lxml")
                    else:
                            link = BeautifulSoup("<a href=\"../\">Table of Contents</a>", "lxml")
                            i.contents[1].contents[1].insert(0, link)
            soup = BeautifulSoup(soup.renderContents(), "lxml")
            for j in soup.findAll("table", attrs={"summary": "Navigation footer"}):
                   if name == "index.html":
                           link = BeautifulSoup("<a href=\"ix01.html\">Index</a>", "lxml")
                   elif name == "ix01.html":
                           link = BeautifulSoup("", "lxml")
                   else:
                           link = BeautifulSoup("<a href=\"../ix01.html\">Index</a>", "lxml")
                   j.contents[0].contents[1].insert(0, link)
                   if name == "ix01.html":
                           link = BeautifulSoup("<a href=\"index.html\">Table of Contents</a>", "lxml")
                   if name == "index.html":
                           link = BeautifulSoup("", "lxml")
                   elif name == "ix01.html":
                           link = BeautifulSoup("<a href=\"index.html\">Table of Contents</a>", "lxml")
                   else:
                           link = BeautifulSoup("<a href=\"../\">Table of Contents</a>", "lxml")
                   j.contents[0].contents[1].insert(0, link)
                   j.contents[1].contents[1].clear()
                   j.contents[1].contents[1].insert(0, link)
                # Now mathjax removed
            p = BeautifulSoup("<h3><a href='/'>Site Home</a></h3><p class='alert alert-danger'>Please see <a href=\"http://caniuse.com/#feat=mathml\">http://caniuse.com/#feat=mathml</a> if your browser supports MathML because certain sections of this book rely on MathML. If your browser does not support MathML please install Firefox from <a href=\"https://www.mozilla.org\">Mozilla</a> because AFAIK Firefox supports MathML.</p>", "lxml")
            soup.body.insert(0, p)
            soup = BeautifulSoup(soup.renderContents(), "lxml")
#                                for i in soup.find_all("pre", "CommonLispLexer"):
#                                        code = BeautifulSoup(highlight(i.string, CommonLispLexer(), HtmlFormatter()))
#                                        i.string.replace_with(code)
            soup = BeautifulSoup(soup.renderContents(), "lxml")
#syntax highlighting is not needed for algebra
#            for i in soup.find_all("pre", "CLexer"):
#                   #print i.string
#                   code = BeautifulSoup(highlight(i.string, CLexer(), HtmlFormatter()), "lxml")
#                   i.string.replace_with(code)
#            soup = BeautifulSoup(soup.renderContents(), "lxml")
#            for i in soup.find_all("pre", "ALexer"):
#                   code = BeautifulSoup(highlight(i.string, CObjdumpLexer(), HtmlFormatter()), "lxml")
#                   i.string.replace_with(code)
#            soup = BeautifulSoup(soup.renderContents(), "lxml")
#            for i in soup.find_all("pre", "MakefileLexer"):
#                   code = BeautifulSoup(highlight(i.string, MakefileLexer(), HtmlFormatter()), "lxml")
#                   i.string.replace_with(code)
            with open(filepath, "w") as f:
                   #print "Hello"
                   f.write(soup.encode(formatter='html'))

findReplace("build/", "mml:", "", "index.html")
findReplace("build/", "mml:", "", "ix01.html")
#print files_list
setup(files_list)
