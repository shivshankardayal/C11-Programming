all:
	xsltproc --xinclude --stringparam html.stylesheet "../css/bootstrap.css ../css/style.css" html.xsl c.xml
	./domp.py
