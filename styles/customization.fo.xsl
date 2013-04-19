<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:d="http://docbook.org/ns/docbook"
  xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exsl="http://exslt.org/common">

  <!-- Points to the official stylesheet distro -->
  <xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl-ns/fo/docbook.xsl" />

  <!--
   * IMPORTANT!
   *
   * Change the paths to the proper locations for your configuration
   *
   * IMPORTANT
   *
   * You need to include both the common highlighting and the specific highlighter for your target, be it FO or HTML
   * In addition, you need to set highlight.source to 1
   *
   * But that's all there should be to it.
   * Iff all paths are set correctly, you should get proper syntax highlighting.
  -->

  <!-- The location of the highlighting configuration -->
  <xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl-ns/highlighting/common.xsl" />
  <xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl-ns/html/highlight.xsl" />

  <!-- Set Highlighting to 1 to activate -->
  <xsl:param name="highlight.source" select="1"/>
</xsl:stylesheet>

