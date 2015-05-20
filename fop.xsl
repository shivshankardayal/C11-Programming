<?xml version='1.0'?> 
<xsl:stylesheet  
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  version="1.0"
    xmlns:d="http://docbook.org/ns/docbook"> 
  <xsl:import href="/opt/local/share/xsl/docbook-xsl-ns/fo/docbook.xsl"/> 
  <xsl:param name="paper.type" select="'B5'"/> 
  <xsl:param name="double.sided" select="1"/>
  <xsl:param name="fop1.extensions" select="1"/>
  <xsl:param name="body.start.indent">
    <xsl:choose>
      <xsl:when test="$fop1.extensions != 0">0pt</xsl:when>
      <xsl:otherwise>4pc</xsl:otherwise>
    </xsl:choose>
  </xsl:param>
  <xsl:attribute-set name="monospace.properties">
    <xsl:attribute name="font-size">9pt</xsl:attribute>
  </xsl:attribute-set>
  <xsl:attribute-set name="monospace.verbatim.properties" use-attribute-sets="verbatim.properties monospace.properties">
    <xsl:attribute name="font-size">9pt</xsl:attribute>
    <xsl:attribute name="wrap-option">wrap</xsl:attribute>
    <xsl:attribute name="hyphenation-character">&#x25BA;</xsl:attribute>
  </xsl:attribute-set>  
  <xsl:attribute-set name="shade.verbatim.style">
    <xsl:attribute name="border">"thin black solid"</xsl:attribute>
  </xsl:attribute-set>
  <xsl:param name="bookmarks.collapse" select="0"></xsl:param>
  <xsl:attribute-set name="verbatim.properties">
    <xsl:attribute name="border-style">solid</xsl:attribute>
    <xsl:attribute name="border-width">1pt</xsl:attribute>
    <xsl:attribute name="border-color">black</xsl:attribute>
    <xsl:attribute name="padding">3pt</xsl:attribute>
  </xsl:attribute-set>
  <!--xsl:template match="d:programlisting[@role='CLexer']">
    <xsl:copy>
      <xsl:attribute name="language">CLexer</xsl:attribute>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="d:programlisting[@role='MakefileLexer']">
    <xsl:copy>
      <xsl:attribute name="language">MakefileLexer</xsl:attribute>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template-->

  <xsl:param name="highlight.source" select="1"></xsl:param>
  <xsl:param name="highlight.xslthl.config">/Users/gannu/Downloads/xslthl-2.1.3/highlighters/xslthl-config.xml</xsl:param>
</xsl:stylesheet>  
