#!/usr/bin/env bash

perl -pi -e s"/lstlisting\}\[firstnumber=1,\]/minted\}\[breaklines=true,frame=single\]\{text\}/g;" pdf/dsa.tex
perl -pi -e s"/end\{lstlisting\}/end\{minted\}/g;" pdf/dsa.tex
perl -pi -e s"/lstlisting\}\[language=c\,firstnumber=1\,\]/minted\}\[breaklines=true,frame=single\]\{c\}/g;" pdf/dsa.tex
perl -pi -e s"/lstlisting\}\[language=cobjdump\,firstnumber=1\,\]/minted\}\[breaklines=true,frame=single\]\{gas\}/g;" pdf/dsa.tex
perl -pi -e s"/\\\begin{document}/\\\lstset{fancyvrb=false}\n\\\usepackage{minted}\n\\\begin{document}/g;" pdf/dsa.tex
perl -pi -e s"/\\\begin{lstlisting}\[firstnumber=1,escapeinside={<:}{:>}\]/\\\begin{minted}\[breaklines=true,frame=single\]{text}/g;" pdf/dsa.tex
