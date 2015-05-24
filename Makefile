html:
	xsltproc --xinclude --stringparam html.stylesheet "../css/bootstrap.min.css ../css/bootstrap-responsive.min.css ../css/styled.min.css" --path "src css" --output build/ html.xsl c.xml
#	perl -pi -e "s/\.pdf\"/\.png\"/g;" src/*.xml
	find . -name "*.html" | xargs perl -pi -e "s/<html>/<!DOCTYPE html>/g;"
	cp -r images build/
	./domp.py
	cp -r build/* /var/www/cd/


pdf:
	dblatex -bxetex -T db2latex -p dblatex.xsl -P preface.tocdepth="1" src/c.xml

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
