html:
	xsltproc --xinclude --stringparam html.stylesheet "../css/bootstrap.min.css ../css/bootstrap-responsive.min.css ../css/style.css" --path "src css" --output build/ html.xsl c.xml
#	perl -pi -e "s/\.pdf\"/\.png\"/g;" src/*.xml
	find . -name "*.html" | xargs perl -pi -e "s/<html>/<!DOCTYPE html>/g;"
	cp -r images build/
	./domp.py


pdf:
#	perl -pi -e "s/\.png\"/\.pdf\"/g;" src/*.xml
	dblatex -bxetex -T db2latex -P preface.tocdepth="1" src/c.xml
