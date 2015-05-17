html:
	xsltproc --xinclude --stringparam html.stylesheet "../css/bootstrap.min.css ../css/bootstrap-responsive.min.css ../css/styled.css" --path "src css" --output build/ html.xsl c.xml
#	perl -pi -e "s/\.pdf\"/\.png\"/g;" src/*.xml
	find . -name "*.html" | xargs perl -pi -e "s/<html>/<!DOCTYPE html>/g;"
	cp -r images build/
	./domp.py
	cp -r build/* /opt/local/share/nginx/html/cd/


pdf:
	dblatex -bxetex -T db2latex -p dblatex.xsl -P preface.tocdepth="1" src/c.xml

latex:
	dblatex -bxetex -T db2latex -p dblatex.xsl -P preface.tocdepth="1" -t tex src/c.xml
	cd src && perl -pi -e "s/\.png/\.pdf/g;" c.tex

fop:
	xsltproc --xinclude --output src/c.fo --stringparam double.sided 1 --stringparam fop1.extensions 1 --stringparam page.height 9in --stringparam page.width 7.5in --stringparam body.start.indent 0pt --stringparam body.font.size 9  /opt/local/share/xsl/docbook-xsl-ns/fo/docbook.xsl src/c.xml
	perl -pi -e "s/png/pdf/g;" src/c.fo
	cd src && fop c.fo c.pdf
