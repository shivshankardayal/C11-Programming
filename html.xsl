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
  <!--xsl:import href="/opt/local//share/xsl/docbook-xsl-ns/html/chunk.xsl" /-->

  <!-- The location of the highlighting configuration -->
  <!--<xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl-ns/highlighting/common.xsl" />
      <xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl-ns/html/highlight.xsl" />-->
  
  <xsl:template name="user.head.content">
    <xsl:copy-of select="document('analytics.js', /)"/>
    <xsl:copy-of select="document('mathjax.js', /)"/>
  </xsl:template>
  <xsl:template name="user.footer.navigation">
    <br/>
    <p style="text-align: center;">&#xa9; 2010, 2015 Shiv S. Dayal. <a href="http://10hash.com">10hash.com</a>.
    GNU FDL license is applicable where not stated.</p>
  </xsl:template>

  <!-- Set Highlighting to 1 to activate -->
  <xsl:param name="highlight.source" select="1"/>
  <xsl:param name="chapter.autolabel" select="1"/>
  <xsl:param name="section.autolabel" select="1"/>
  <xsl:param name="use.extensions" select="1"/>
  <xsl:param name="textinsert.extension" select="1"/>
  <xsl:param name="tablecolumns.extension" select="1"/>
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
  </xsl:template>
  <xsl:template match="d:programlisting[@role]" mode="class.value">
    <xsl:value-of select="@role"/>
  </xsl:template>
  <xsl:template name="footer.navigation">
    <xsl:param name="prev" select="/d:foo"/>
    <xsl:param name="next" select="/d:foo"/>
    <xsl:param name="nav.context"/>

    <xsl:variable name="home" select="/*[1]"/>
    <xsl:variable name="up" select="parent::*"/>

    <xsl:variable name="row1" select="count($prev) &gt; 0
                                      or count($up) &gt; 0
                                      or count($next) &gt; 0"/>

    <xsl:variable name="row2" select="($prev and $navig.showtitles != 0)
                                      or (generate-id($home) != generate-id(.)
                                      or $nav.context = 'toc')
                                      or ($chunk.tocs.and.lots != 0
                                      and $nav.context != 'toc')
                                      or ($next and $navig.showtitles != 0)"/>

    <xsl:if test="$suppress.navigation = '0' and $suppress.footer.navigation = '0'">
      <div class="navfooter">
        <xsl:if test="$footer.rule != 0">
          <hr/>
        </xsl:if>

        <xsl:if test="$row1 or $row2">
          <table width="100%" summary="Navigation footer">
            <xsl:if test="$row1">
              <tr>
                <td width="40%" align="{$direction.align.start}">
                  <xsl:if test="count($prev)>0">
                    <a accesskey="p">
                      <xsl:attribute name="href">
                        <xsl:call-template name="href.target">
                          <xsl:with-param name="object" select="$prev"/>
                        </xsl:call-template>
                      </xsl:attribute>
                      <xsl:call-template name="navig.content">
                        <xsl:with-param name="direction" select="'prev'"/>
                      </xsl:call-template>
                    </a>
                  </xsl:if>
                  <xsl:text>&#160;</xsl:text>
                </td>
                <td width="20%" align="center">
                  <!--xsl:choose>
                    <xsl:when test="count($up)&gt;0
                                    and generate-id($up) != generate-id($home)">
                      <a accesskey="u">
                        <xsl:attribute name="href">
                          <xsl:call-template name="href.target">
                            <xsl:with-param name="object" select="$up"/>
                          </xsl:call-template>
                        </xsl:attribute>
                        <xsl:call-template name="navig.content">
                          <xsl:with-param name="direction" select="'up'"/>
                        </xsl:call-template>
                      </a>
                    </xsl:when>
                    <xsl:otherwise>&#160;</xsl:otherwise>
                  </xsl:choose-->
                </td>
                <td width="40%" align="{$direction.align.end}">
                  <xsl:text>&#160;</xsl:text>
                  <xsl:if test="count($next)>0">
                    <a accesskey="n">
                      <xsl:attribute name="href">
                        <xsl:call-template name="href.target">
                          <xsl:with-param name="object" select="$next"/>
                        </xsl:call-template>
                      </xsl:attribute>
                      <xsl:call-template name="navig.content">
                        <xsl:with-param name="direction" select="'next'"/>
                      </xsl:call-template>
                    </a>
                  </xsl:if>
                </td>
              </tr>
            </xsl:if>

            <xsl:if test="$row2">
              <tr>
                <td width="40%" align="{$direction.align.start}" valign="top">
                  <xsl:if test="$navig.showtitles != 0">
                    <xsl:apply-templates select="$prev" mode="object.title.markup"/>
                  </xsl:if>
                  <xsl:text>&#160;</xsl:text>
                </td>
                <td width="20%" align="center">
                  <xsl:choose>
                    <xsl:when test="$home != . or $nav.context = 'toc'">
                      <a accesskey="h">
                        <xsl:attribute name="href">
                          <xsl:call-template name="href.target">
                            <xsl:with-param name="object" select="$home"/>
                          </xsl:call-template>
                        </xsl:attribute>
                        <xsl:call-template name="navig.content">
                          <xsl:with-param name="direction" select="'home'"/>
                        </xsl:call-template>
                      </a>
                      <xsl:if test="$chunk.tocs.and.lots != 0 and $nav.context != 'toc'">
                        <xsl:text>&#160;|&#160;</xsl:text>
                      </xsl:if>
                    </xsl:when>
                    <xsl:otherwise>&#160;</xsl:otherwise>
                  </xsl:choose>

                  <xsl:if test="$chunk.tocs.and.lots != 0 and $nav.context != 'toc'">
                    <a accesskey="t">
                      <xsl:attribute name="href">
                        <xsl:value-of select="$chunked.filename.prefix"/>
                        <xsl:apply-templates select="/*[1]"
                                             mode="recursive-chunk-filename">
                          <xsl:with-param name="recursive" select="true()"/>
                        </xsl:apply-templates>
                        <xsl:text>-toc</xsl:text>
                        <xsl:value-of select="$html.ext"/>
                      </xsl:attribute>
                      <xsl:call-template name="gentext">
                        <xsl:with-param name="key" select="'nav-toc'"/>
                      </xsl:call-template>
                    </a>
                  </xsl:if>
                </td>
                <td width="40%" align="{$direction.align.end}" valign="top">
                  <xsl:text>&#160;</xsl:text>
                  <xsl:if test="$navig.showtitles != 0">
                    <xsl:apply-templates select="$next" mode="object.title.markup"/>
                  </xsl:if>
                </td>
              </tr>
            </xsl:if>
          </table>
        </xsl:if>
      </div>
    </xsl:if>
  </xsl:template>
<xsl:template name="header.navigation">
  <xsl:param name="prev" select="/d:foo"/>
  <xsl:param name="next" select="/d:foo"/>
  <xsl:param name="nav.context"/>

  <xsl:variable name="home" select="/*[1]"/>
  <xsl:variable name="up" select="parent::*"/>

  <xsl:variable name="row1" select="$navig.showtitles != 0"/>
  <xsl:variable name="row2" select="count($prev) &gt; 0
                                    or (count($up) &gt; 0 
                                        and generate-id($up) != generate-id($home)
                                        and $navig.showtitles != 0)
                                    or count($next) &gt; 0"/>

  <xsl:if test="$suppress.navigation = '0' and $suppress.header.navigation = '0'">
    <div class="navheader">
      <xsl:if test="$row1 or $row2">
        <table width="100%" summary="Navigation header" >
          <xsl:if test="$row1">
            <tr>
              <th colspan="3" align="center" style="text-align: center; font-weight:300; padding-right:8px">
                <xsl:apply-templates select="." mode="object.title.markup"/>
              </th>
            </tr>
          </xsl:if>

          <xsl:if test="$row2">
            <tr>
              <td width="20%" align="{$direction.align.start}">
                <xsl:if test="count($prev)>0">
                  <a accesskey="p">
                    <xsl:attribute name="href">
                      <xsl:call-template name="href.target">
                        <xsl:with-param name="object" select="$prev"/>
                      </xsl:call-template>
                    </xsl:attribute>
                    <xsl:call-template name="navig.content">
                      <xsl:with-param name="direction" select="'prev'"/>
                    </xsl:call-template>
                  </a>
                </xsl:if>
                <xsl:text>&#160;</xsl:text>
              </td>
              <th width="60%" align="center" style="text-align: center; font-weight:normal">
                <xsl:choose>
                  <xsl:when test="count($up) > 0
                                  and generate-id($up) != generate-id($home)
                                  and $navig.showtitles != 0">
                    <!--xsl:apply-templates select="$up" mode="object.title.markup"/-->
                  </xsl:when>
                  <xsl:otherwise>&#160;</xsl:otherwise>
                </xsl:choose>
              </th>
              <td width="20%" align="{$direction.align.end}">
                <xsl:text>&#160;</xsl:text>
                <xsl:if test="count($next)>0">
                  <a accesskey="n">
                    <xsl:attribute name="href">
                      <xsl:call-template name="href.target">
                        <xsl:with-param name="object" select="$next"/>
                      </xsl:call-template>
                    </xsl:attribute>
                    <xsl:call-template name="navig.content">
                      <xsl:with-param name="direction" select="'next'"/>
                    </xsl:call-template>
                  </a>
                </xsl:if>
              </td>
            </tr>
          </xsl:if>
        </table>
      </xsl:if>
      <xsl:if test="$header.rule != 0">
        <hr/>
      </xsl:if>
    </div>
  </xsl:if>
</xsl:template>

</xsl:stylesheet>

