all:
	xsltproc --xinclude html.xsl c.xml
	./domp.py
