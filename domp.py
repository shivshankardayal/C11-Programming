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
				s = s.replace("index.html", "")
				soup = BeautifulSoup(s)
				p=''
				n=''
				pl=''
				nl=''
				
				for i in soup.find_all("table", attrs={"summary": "Navigation footer"}):
					n=i.contents[1].contents[2].string
					p=i.contents[1].contents[0].string
				for j in soup.find_all("a", attrs={"accesskey": "n"}, limit=1):
					s = BeautifulSoup(str(j))
					if len(str(s.a["href"])) != 0:
						nl = str(s.a["href"])
				for j in soup.find_all("a", attrs={"accesskey": "p"}, limit=1):
					s = BeautifulSoup(str(j))
					if len(str(s.a["href"])) != 0:
						pl = str(s.a["href"])

				if p == u'\xa0':
					p = ''
				if n == u'\xa0':
					n = ''

				title = soup.title.string

				#print title

				toc = ''
				for i in soup.find_all("div", "toc"):
					toc = str(i)

				#print toc

				navbar = '<div id="navbar" class="navbar navbar-fixed-top">  \
  <div class="navbar-inner">  \
    <div class="container-fluid">  \
    <a class="brand" href="http://libreprogramming.org/">Home</a>  \
    <a class="brand" href="http://libreprogramming.org/books/">Books</a>  \
<ul class="nav">\
  <li class="dropdown">  \
    <a href="#"  \
          class="dropdown-toggle"  \
          data-toggle="dropdown">' + title + \
          '<b class="caret"></b>  \
    </a>  \
    <ul class="dropdown-menu">' + toc +' \
    </ul>  \
  </li>  \
</ul> \
<ul class="nav">\
'

				if p != '':
					navbar += '<li><a href="' + pl + '">&lt;&lt; ' + p + '</a><li>'
				if n != '':
					navbar += '<li><a href="' + nl + '">' + n + ' >></a><li>'
				navbar += '\
</ul>\
    </div>  \
  </div>  \
</div>\
'
				tweet_google = '<a href="https://twitter.com/share" class="twitter-share-button">Tweet</a>\
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?\'http\':\'https\';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+\'://platform.twitter.com/widgets.js\';fjs.parentNode.insertBefore(js,fjs);}}(document, \'script\', \'twitter-wjs\');</script>' + \
'<script type="text/javascript" src="https://apis.google.com/js/plusone.js"></script>\
<!-- Place this tag where you want the +1 button to render. -->\
<g:plusone size="medium"></g:plusone>'
#print navbar
				soup.body.insert(0, navbar)
				#soup.body.insert(1, tweet_google)

				for i in soup.find_all("pre", "CommonLispLexer"):
					i.string.replace_with(highlight(i.string, CommonLispLexer(), HtmlFormatter()))

				for i in soup.find_all("pre", "CLexer"):
					i.string.replace_with(highlight(i.string, CLexer(), HtmlFormatter()))

				for i in soup.find_all("pre", "MakefileLexer"):
					i.string.replace_with(highlight(i.string, MakefileLexer(), HtmlFormatter()))
			with open(filepath, "w") as f:
				f.write(soup.encode(formatter=None))

findReplace(".", "mml:", "", "index.html")
findReplace(".", "mml:", "", "ix01.html")
