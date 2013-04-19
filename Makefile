all:
	xsltproc html.xsl c.xml
	./domp.py
