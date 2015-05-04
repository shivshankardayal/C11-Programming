#!/usr/bin/env python

import lxml.html
from lxml import etree
import sys, os, fnmatch
from pygments import highlight
from pygments.lexers import *
from pygments.formatters import HtmlFormatter
import copy

def findReplace(directory, find, replace, filePattern):
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
                s = s.replace(find, replace)
                s = s.replace("index.html", "")
                html = lxml.html.fromstring(s)
                p=''
                n=''
                pl=''
                nl=''

                elements = html.xpath("//table[@summary]")
#                print etree.tostring(elements[0])
#                print etree.tostring(elements[1])

                centers = (elements[0].xpath("//table/tr/th"))
                centers[0].text = '<a href="../ix01.html">Index</a>'
                centers[1].text = '<a href="../index.html">Home</a>'
#                print etree.tostring(centers[0])
#                print etree.tostring(centers[1])

                centers = (elements[1].xpath("//table/tr/td[@align='center']"))
                centers[0].text = '<a href="../ix01.html">Index</a>'
#                print etree.tostring(centers[0])
#                print etree.tostring(centers[1])

                body = html.xpath("//body")
#                print body
                
                header = etree.Element("p")
                header.text = "Please see <a href=\"http://caniuse.com/#feat=mathml\">;http://caniuse.com/#feat=mathml&</a> if your browser supports MathML because certain sections of this book rely on MathML."
                body[0].insert(0, header)

#                print etree.tostring(header)
#                print etree.tostring(html, pretty_print=True)

                pres = html.xpath("//pre[@class='CommonLispLexer']")
                l = []
                for pre in pres:
                    div = etree.Element("div")
                    div.text = highlight(pre.text, CommonLispLexer(), HtmlFormatter())
                    l.append(div)
                pres = copy.deepcopy(l)
                pres1 = html.xpath("//pre[@class='MakefileLexer']")
                l = []
                for pre in pres1:
                    div = etree.Element("div")
                    div.text = highlight(pre.text, MakefileLexer(), HtmlFormatter())
                    l.append(div)
                pres1 = copy.deepcopy(l)

                pres2 = html.xpath("//pre[@class='CLexer']")
                l = []
                for pre in pres:
                    div = etree.Element("div")
                    div.text = highlight(pre.text, CLexer(), HtmlFormatter())
                    l.append(div)
                pres2 = copy.deepcopy(l)

                with open(filepath, "w") as f:
                    f.write(etree.tostring(html, encoding="unicode", method='text', pretty_print=True))

findReplace("build/", "mml:", "", "index.html")
findReplace("build/", "mml:", "", "ix01.html")
