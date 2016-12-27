<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xsl:stylesheet [
	<!ENTITY navWidth "30ex">
	<!ENTITY navColor "#999">
	<!ENTITY navBgColor "#333">
	<!ENTITY bgColor "#fff">
	<!ENTITY addedColor "#dfd">
	<!ENTITY deletedColor "#fdd">
	<!ENTITY changedColor "#ffb">
	<!ENTITY commonColor "#ddf">
	<!ENTITY sameTrebuchet "'Trebuchet MS', Helvetica, sans-serif">
	<!ENTITY sameArial "Arial, Helvetica, sans-serif">
	<!ENTITY allApiAncestors "ancestor::Module|ancestor::Class|ancestor::Sub-Class">
]>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>

<xsl:output doctype-system="about:legacy-compat" method="html" encoding="utf-8" />

<xsl:template match="LiveAPI">
	<xsl:variable name="title">
		Live API
		<xsl:choose>
			<xsl:when test="@compare"><xsl:value-of select="substring-before(@version, '-')" />→<xsl:value-of select="substring-after(@version, '-')" /> comparison</xsl:when>
			<xsl:otherwise>version <xsl:value-of select="@version" /></xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<html>
		<head>
			<meta charset="utf-8" />
			<title><xsl:value-of select="$title" /></title>
			<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
			<!--script src="jquery-1.12.4.min.js"></script-->
			<script src="jquery.singlePageNav-multilevel.js"></script>
			<script>
function client_height () {
	return Math.min (
		window.innerHeight,
		document.documentElement.clientHeight,
		document.body.clientHeight
	);
}
function show_module_content () {
	$("#Live").removeClass ("collapsed");
	var id = $(this).attr ("href");
	var $div = $(id);
	$div.removeClass ("collapsed");
	$div.find('.Module, .Class, .Sub-Class').addClass ("collapsed");
	return false;
}
function toggle_folding () {
	var $thisDiv = $(this).parent ();
	if ($thisDiv.hasClass('collapsed')) {
		$thisDiv.toggleClass ("collapsed");
	} else {
		$thisDiv.addClass ("collapsed");
		$thisDiv.find('.Module, .Class, .Sub-Class').addClass ("collapsed");
	}
}
function expand_recursively () {
	var $thisDiv = $(this).parent ();
	$thisDiv.removeClass ("collapsed");
	$thisDiv.find('.Module, .Class, .Sub-Class').removeClass ("collapsed");
	return false;
}
function compare_switch (event) {
	if (event.which == 1) { // left button
		if (event.ctrlKey)
			$(this).toggleClass ("checked");
		else {
			$("#compare-switch span").removeClass ("checked");
			$(this).addClass ("checked");
		}
	} else // if (event.which == 3) // right button
		$(this).toggleClass ("checked");
	if (!$("#compare-switch span.checked").length)
		$("#compare-switch span").addClass ("checked");
	
	var added = $("#added").hasClass ("checked");
	var changed = $("#changed").hasClass ("checked");
	var deleted = $("#deleted").hasClass ("checked");
	var common = $("#common").hasClass ("checked");
	var $added = $(".added");
	var $changed = $(".changed");
	var $deleted= $(".deleted");
	var $common = $(".common");
	if (!added) $added.css ("display", "none");
	if (!changed) $changed.css ("display", "none");
	if (!deleted) $deleted.css ("display", "none");
	if (!common) $common.css ("display", "none");
	if (added) $added.css ("display", "");
	if (changed) $changed.css ("display", "");
	if (deleted) $deleted.css ("display", "");
	if (common) $common.css ("display", "");
	//$("#Live &gt; h2").trigger ("contextmenu");
	return false;
}
$(document).ready (
	function () {
		var $h2 = $("div h2");
		$h2.on ("click", toggle_folding);
		$h2.on ("contextmenu", expand_recursively);
		$("#nav a").on ("click", show_module_content);
		$("#nav").singlePageNav ({offset: 1/3 * client_height ()}); // make navigation
		$("#compare-switch span").on ("click", compare_switch);
		$("#compare-switch span").on ("contextmenu", compare_switch);
	}
);
			</script>
			<style>
body {
	font-family: <!--Calibri-->
		&sameTrebuchet;;
		font-size: 10.5pt;
	margin: 0;
	margin-left: &navWidth;;
	padding: 3%;
	background-color: &bgColor;;
}

/*****************************************************************************/
ul {
	padding: 0;
	margin: 0;
	list-style-type: none;
}
#nav {
	width: &navWidth;;
	background-color: &navBgColor;;
	position: fixed;
	left: 0; top: 0; bottom: 0;
	overflow-x: hidden;
	overflow-y: auto;
	padding: 1.5ex 0;
}
#nav:hover .added {background-color: #252;}
#nav:hover .deleted {background-color: #522;}
#nav:hover .common {background-color: &navBgColor;;}
#nav:hover .added.common, #nav:hover .deleted.common {background-color: #441;}
#nav a {
	text-decoration: none;
	display: block; /* чтобы растянуть на всю ширину */
	padding-left: 2ex;
	color: &navColor;; /* default */
	;
		line-height: 14.3pt;
}
#nav a[href="#Live"] {color: #fff;}
#nav a[href="#Live"]:hover, #nav a[href="#Live"].current {background-color: #fff !important;}
#nav a:hover, #nav a.current {color: &navBgColor; !important; background-color: &navColor;;} /* default */
<xsl:for-each select="descendant::Module/Module"><!-- По всем дочерним модулям главного модуля -->
#nav a[href="#Live-<xsl:value-of select="@name" />"]:hover,
#nav a[href="#Live-<xsl:value-of select="@name" />"] ~ ul a:hover,
#nav a[href="#Live-<xsl:value-of select="@name" />"].current,
#nav a[href="#Live-<xsl:value-of select="@name" />"] ~ ul a.current
	{background-color: hsl(<xsl:value-of select="round (360 * (position () - 1) div count(../*))" />, 100%, 94%) !important;}
#nav a[href="#Live-<xsl:value-of select="@name" />"].current-module,
#nav a[href="#Live-<xsl:value-of select="@name" />"].current-module ~ ul a,
#nav:hover a[href="#Live-<xsl:value-of select="@name" />"]
	{color: hsl(<xsl:value-of select="round (360 * (position () - 1) div count(../*))" />, 100%, 94%);}
</xsl:for-each>
/*****************************************************************************/

#header {margin-bottom: 3ex;}

h1, h2, h3 {margin: 0; color: #333;}
	h1, h2 {font-family: &sameArial;; line-height: 135%;}

#compare-switch {float:right;}
#compare-switch span {
	border: solid 1pt;
	margin: 0;
	padding: 1pt 10pt;
	cursor: pointer;
}
#compare-switch #added {border-color: &addedColor;;}
#compare-switch #changed {border-color: &changedColor;;}
#compare-switch #deleted {border-color: &deletedColor;;}
#compare-switch #common {border-color: &commonColor;;}
#added:hover {background-color: &addedColor;;}
#changed:hover {background-color: &changedColor;;}
#deleted:hover {background-color: &deletedColor;;}
#common:hover {background-color: &commonColor;;}
#added.checked {background-color: &addedColor;;}
#changed.checked {background-color: &changedColor;;}
#deleted.checked {background-color: &deletedColor;;}
#common.checked {background-color: &commonColor;;}
#added.checked:hover {background-color: #bfb;}
#changed.checked:hover {background-color: #ff7;}
#deleted.checked:hover {background-color: #fbb;}
#common.checked:hover {background-color: #bbf;}

.Module, .Class, .Sub-Class {
	padding: 1ex 0 1ex 5ex;
	margin-top: 1ex;
	border: dotted 1pt transparent;
}
div.current {border-color: hsla(0, 0%, 0%, 0.1333);}
.collapsed div {display: none;}

/*****************************************************************************/
h2 {
	cursor: pointer;
	position: relative;
	left: -1.5ex;
	background-color: #eee;
	border: solid #ddd;
	border-width: 1pt 0;
}
<xsl:for-each select="descendant::Module/Module">
#Live-<xsl:value-of select="@name" /> h2 {
	background-color: hsl(<xsl:value-of select="round (360 * (position () - 1) div count(../*))" />, 50%, 94%);
	border-color: hsl(<xsl:value-of select="round (360 * (position () - 1) div count(../*))" />, 50%, 87%);
}</xsl:for-each>
h2:before {content: "− ";}
.collapsed h2 {
	background-color: transparent !important;
	display: inline;
	border: none;
}
.collapsed h2:before {content: "+ ";}
.count {
	font-family: <!--"Calibri Light"-->
		&sameArial;; opacity: 0.5;  filter: alpha(opacity=50);
	font-weight: normal;
	font-size: smaller;
	display: none;
}
.collapsed .count {display: inline;}
.type {
	font-weight: normal;
	font-style: italic;
	font-size: smaller;
	margin-left: 1ex;
	opacity: 0.5;  filter: alpha(opacity=50);
}
/*****************************************************************************/

.member {padding: 1pt 10pt; margin: 1ex;/* border-radius: 1ex;*/}
.name {font-weight: bold;}
<!--h3 {font-size: large;}-->
.listener h3 {font-weight: normal;}
p {
	color: #777;
	font-style: italic;
	margin: 0;
	/*border-radius: 1ex;*/
}
.member p {padding-left: 20pt; font-style: normal;}
.member:active .Format {display: none;}
.Cpp-Signature {display: none;}
.member:active .Cpp-Signature {display: block;}
p.Description {font-style: italic; color: #000;}

.prefix {
	font-weight: normal;
	font-size: smaller;
	display: none;
}
.listener h3 .prefix {<!--font-family: "Calibri Light";--> opacity: 0.5;  filter: alpha(opacity=50);}
.member:active .prefix {display: inline;}

.hidden {display: none;}
div .added {background-color: &addedColor;;}
div .deleted {background-color: &deletedColor;;}
.added.common, .deleted.common {background-color: transparent;}
.added.common.collapsed, .deleted.common.collapsed {background-color: &changedColor;;}
			</style>
		</head>
		<body>
			<xsl:apply-templates select="Module">
				<xsl:with-param name="nav" select="1" />
				<xsl:with-param name="root" select="1" />
			</xsl:apply-templates>
			<div id="header">
				<xsl:if test="@compare">
					<div id="compare-switch">
						<span id="added" class="checked">Added</span>
						<span id="changed" class="checked">Changed</span>
						<span id="deleted" class="checked">Deleted</span>
						<span id="common" class="checked">Common</span>
					</div>
				</xsl:if>
				<h1><xsl:value-of select="$title" /></h1>
				<xsl:apply-templates select="Doc" />
			</div>
			<xsl:apply-templates select="Module" />
		</body>
	</html>
</xsl:template>



<xsl:template match="Module|Class|Sub-Class">
	<xsl:param name="nav"/>
	<xsl:param name="root"/>
	<xsl:choose>
	
		<xsl:when test="$nav = 1">
		
			<ul>
				<xsl:if test="$root = 1">
					<xsl:attribute name="id">nav</xsl:attribute>
				</xsl:if>
				<li>
					<xsl:attribute name="class">
						<xsl:if test="@name != 'Live' and ../@name != 'Live'">hidden </xsl:if><xsl:value-of select="@compare" />
					</xsl:attribute>
					<a style="padding-left: {2 * (count (&allApiAncestors;) + 1)}ex;">
						<xsl:attribute name="href">
							<xsl:text>#</xsl:text><xsl:for-each select="&allApiAncestors;"><xsl:value-of select="@name" />-</xsl:for-each><xsl:value-of select="@name" />
						</xsl:attribute>
						<xsl:value-of select="@name" />
					</a>
					<xsl:apply-templates select="Module|Class|Sub-Class">
						<xsl:with-param name="nav" select="1" />
					</xsl:apply-templates>
				</li>
			</ul>
			
		</xsl:when>
		
		<xsl:otherwise>
		
			<div>
				<xsl:attribute name="id">
					<xsl:for-each select="&allApiAncestors;"><xsl:value-of select="@name" />-</xsl:for-each><xsl:value-of select="@name" />
				</xsl:attribute>
				<xsl:attribute name="class">
					<xsl:value-of select="name ()" /><xsl:text> </xsl:text><xsl:value-of select="@compare" />
				</xsl:attribute>
				<h2>
					<xsl:value-of select="@name" />
					<span class="count">
						<xsl:variable name="common" select="./*[name () != 'Doc' and (contains (@compare, 'common') or not (@compare))]" />
						<xsl:variable name="added" select="./*[name () != 'Doc' and @compare = 'added']" />
						<xsl:variable name="deleted" select="./*[name () != 'Doc' and @compare = 'deleted']" />
						(<xsl:value-of select="count ($common)" /><xsl:if test="$deleted">−<xsl:value-of select="count ($deleted)" /></xsl:if><xsl:if test="$added">+<xsl:value-of select="count ($added)" /></xsl:if>)
					</span>
					<span class="type"><xsl:value-of select="name ()" /></span>
				</h2>
				<xsl:apply-templates select="Doc" />
				<xsl:apply-templates select="Module" />
				<xsl:apply-templates select="Class" />
				<xsl:apply-templates select="Sub-Class" />
				<xsl:apply-templates select="Property|Value|Built-In|Method" />
			</div>
			
		</xsl:otherwise>
		
	</xsl:choose>
</xsl:template>



<xsl:template match="Property|Value|Built-In|Method">
	<div>
		<xsl:attribute name="class">
			member <xsl:if test="contains (@name, '_listener')">listener </xsl:if><xsl:value-of select="@compare" />
		</xsl:attribute>
		<h3>
			<span class="prefix">
				<xsl:for-each select="&allApiAncestors;"><xsl:value-of select="@name" />.</xsl:for-each>
			</span>
			<xsl:value-of select="@name" /> <span class="type"><xsl:value-of select="name ()" /></span>
		</h3>
		<xsl:apply-templates select="Doc" />
	</div>
</xsl:template>

<xsl:template match="Doc">
	<p>
		<xsl:attribute name="class">
			<xsl:value-of select="@type" /><xsl:text> </xsl:text><xsl:value-of select="@compare" />
		</xsl:attribute>
		<xsl:if test="@type = 'Cpp-Signature'">C++ signature: </xsl:if><xsl:value-of select="text ()" />
	</p>
</xsl:template>

</xsl:stylesheet>
