html: src/*.xml html.xsl Makefile
#	xsltproc --xinclude --stringparam html.stylesheet "../css/bootstrap.min.css ../css/bootstrap-responsive.min.css ../css/styled.min.css ../css/highlight.css" --path "src css" --output build/ html.xsl c.xml
	xsltproc --xinclude --stringparam html.stylesheet "../css/one.min.css" --path "src css" --output build/ html.xsl c.xml
#	perl -pi -e "s/\.pdf\"/\.png\"/g;" src/*.xml
	find . -name "*.html" | xargs perl -pi -e "s/<html>/<!DOCTYPE html>/g;"
	find . -name "*.html" | xargs perl -pi -e "s/<meta/<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><meta/g;"
	cp -r images build/
	./domp.py
	cp -r build/* /var/www/c-programming/


pdf: src/*.xml dblatex.xsl Makefile
	rm -rf pdf
	cp -r src pdf	
	perl -pi -e "s/\.png\"/\.pdf\"/g;" pdf/*.xml	
	dblatex -bxetex -T db2latex -p dblatex.xsl -P preface.tocdepth="1" pdf/c.xml

latex:
	dblatex -bxetex -T db2latex -p dblatex.xsl -P preface.tocdepth="1" -t tex src/c.xml
	cd src && perl -pi -e "s/\.png/\.pdf/g;" c.tex

fop:
#	cd src && xmllint --xinclude c.xml>resolvedc.xml
	xsltproc --xinclude --output src/c.fo fop.xsl src/c.xml
	perl -pi -e "s/png/pdf/g;" src/c.fo
#	./fop.py
#	perl -pi -e "s/<html><body>//g;" src/c.fo
#	perl -pi -e "s/<\/body><\/html>//g;" src/c.fo
	cd src && fop c.fo c.pdf 

epub: src/*.xml epub.xsl Makefile
	xsltproc --xinclude --stringparam html.stylesheet "../css/bootstrap.min.css ../css/bootstrap-responsive.min.css ../css/styled.min.css" --path "src css" epub.xsl c.xml
	cp -r images OEBPS
	./epub.py
	zip -r c.epub mimetype css META-INF/ OEBPS/
