<?xml version='1.0' encoding="iso-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version='1.0'>
  <!-- See:
       http://fossies.org/linux/privat/dblatex-0.3.4.tar.gz:a/dblatex-0.3.4/docs/xhtml/manual/sec-pagination-params.html
       for more information on how to use the following parameters -->
  <xsl:param name="geometry.options">twoside</xsl:param>
  <xsl:param name="paper.type">a4paper</xsl:param>

  <!-- Include the colophon in the Table of Contents -->
  <xsl:param name="colophon.tocdepth">1</xsl:param>

  <!-- Don't show the 'collaborators' section -->
  <xsl:param name="doc.collab.show">0</xsl:param>

  <!-- List *everything* in the table of contents -->
  <xsl:param name="doc.lot.show"></xsl:param>

  <!-- Fix the blank note image -->
  <xsl:param name="figure.note">note</xsl:param>
  <xsl:param name="filename.as.url">1</xsl:param>

  <!-- Include page numbers and titles in cross references -->
  <!--xsl:param name="insert.xref.page.number">yes</xsl:param-->
  <xsl:param name="xref.with.number.and.title" select="1"/>

  <!-- Blue - EVERYWHERE! -->
  <xsl:param name="latex.hyperparam">colorlinks,linkcolor=blue,anchorcolor=blue,urlcolor=blue</xsl:param>
  <!-- Black - Test print version -->
  <!--xsl:param name="latex.hyperparam">colorlinks,linkcolor=black,anchorcolor=black,urlcolor=black</xsl:param-->

  <!-- Don't include the revision history block -->
  <xsl:param name="latex.output.revhistory">0</xsl:param>

  <!-- Condense copyright years into a smaller 'range' if possible -->
  <xsl:param name="make.year.ranges" select="1" />

  <!-- Put a break after terms so that the definition begins on the following line -->
  <xsl:param name="term.breakline">1</xsl:param>

  <!-- Experimenting with different class styles. I like the way the headers are done in the book class -->
  <!--xsl:param name="latex.class.book">book</xsl:param-->

  <xsl:param name="xref.hypermarkup" select="1"/>
  <xsl:param name="refentry.numbered">1</xsl:param>

  <xsl:param name="page.margin.top">.5in</xsl:param>
  <xsl:param name="page.margin.bottom">.5in</xsl:param>
  <xsl:param name="body.master.font">9pt</xsl:param>
  
  <!-- Font's available at: -->
  <!-- http://iweb.dl.sourceforge.net/project/sourcesans.adobe/SourceSansPro_FontsOnly-1.050.zip -->
  <!-- http://iweb.dl.sourceforge.net/project/sourcecodepro.adobe/SourceCodePro_FontsOnly-1.017.zip -->
  <xsl:param name="xetex.font">
    <xsl:text>\setmainfont[Ligatures=TeX,Scale=1]{Latin Modern Roman}
    </xsl:text>
    <xsl:text>\setsansfont[Ligatures=TeX,Scale=.95]{Latin Modern Sans}
    </xsl:text>
    <xsl:text>\setmonofont{Latin Modern Mono}
    </xsl:text>
  </xsl:param>
</xsl:stylesheet>
