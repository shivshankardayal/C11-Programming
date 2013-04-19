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
				s = f.read()
				s = s.replace(find, replace)
				soup = BeautifulSoup(s)

				for i in soup.find_all("pre", "CommonLispLexer"):
					i.string.replace_with(highlight(i.string, CommonLispLexer(), HtmlFormatter()))

				for i in soup.find_all("pre", "CLexer"):
					i.string.replace_with(highlight(i.string, CLexer(), HtmlFormatter()))

				for i in soup.find_all("pre", "MakefileLexer"):
					i.string.replace_with(highlight(i.string, MakefileLexer(), HtmlFormatter()))
			with open(filepath, "w") as f:
				f.write(soup.encode(formatter=None))
				#f.write(BeautifulSoup(soup.prettify(formatter=None)).encode(formatter=None))
					

findReplace(".", "mml:", "", "index.html")
