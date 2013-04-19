<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:d="http://docbook.org/ns/docbook"
  xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exsl="http://exslt.org/common">

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

  <!-- Use the official stylesheet distro -->
  <xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl-ns/html/chunk.xsl" />

  <!-- The location of the highlighting configuration -->
  <!--<xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl-ns/highlighting/common.xsl" />
  <xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl-ns/html/highlight.xsl" />-->
 
 <xsl:param name="html.stylesheet" select="'../css/style.css'" />
 <xsl:template name="user.head.content">
  <script src="../css/analytics.js" type="text/javascript"></script>
 </xsl:template>
 <xsl:template name="user.footer.navigation">
  <p style="text-align: center;">&#x00A9; 2010, 2013 Shiv S. Dayal. <a href="http://libreprogramming.org">libreprogramming.org</a>.
   GNU FDL license is applicable where not stated.</p>
 </xsl:template>

  <!-- Set Highlighting to 1 to activate -->
  <xsl:param name="highlight.source" select="1"/>
 <xsl:param name="chapter.autolabel" select="1"/>
 <xsl:param name="section.autolabel" select="1"/>
 <xsl:param name="use.extensions" select="1"/>
  <xsl:param name="textinsert.extension" select="1"/>
 <xsl:param name="section.label.includes.component.label" select="1"/>
 <xsl:param name="chunk.section.depth" select="0"/>
 <xsl:param name="toc.section.depth" select="4"/>
 <xsl:template name="section.titlepage.before.recto">
  <xsl:variable name="level">
   <xsl:call-template name="section.level"/>
  </xsl:variable>
  <xsl:variable name="chunkfn">
   <xsl:apply-templates mode="chunk-filename" select="."/>
  </xsl:variable>
  
  <xsl:if test="$level &gt; $chunk.section.depth">
   <p class="returntotop">
    <a href="../../{$chunkfn}">
     <xsl:text>Return to top</xsl:text>
    </a>
   </p>
  </xsl:if>
 </xsl:template>
<xsl:template match="d:programlisting[@role]" mode="class.value">
  <xsl:value-of select="@role"/>
 </xsl:template>
</xsl:stylesheet>

