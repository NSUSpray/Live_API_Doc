# -*- coding: utf-8 -*-
import sys, os, codecs, re

reload (sys)
sys.setdefaultencoding ('utf-8')


content = ''
content += '''<!DOCTYPE html>
<meta charset="utf-8">
<title>Live API documentation</title>
<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
<script>
function radio_proc () {
    var primaryValue = $("[name='primary']:checked").val ();
    var targetValue = $("[name='target']:checked").val ();
    var $submit = $(":submit");
    if (targetValue > primaryValue) {
        $submit.removeAttr ("disabled");
    } else {
        $submit.attr ("disabled", true);
    }
    if ($(this).attr ("name") == "primary") {
        var $targets = $("[name='target']");
        $targets.each (function () {
            if ($(this).val () <= primaryValue)
                $(this).addClass ("impossible");
            else
                $(this).removeClass ("impossible");
        });
    } else {
        var $primaries = $("[name='primary']");
        $primaries.each (function () {
            if ($(this).val () >= targetValue)
                $(this).addClass ("impossible");
            else
                $(this).removeClass ("impossible");
        });
    }
}
$(document).ready (
    function () {
        $(":radio").on ("change", radio_proc);
        $("form").submit (function () {
            var primaryValue = $("[name='primary']:checked").val ();
            var targetValue = $("[name='target']:checked").val ();
            function clearNum (version) {
                return version.split(".").map(
                    function (num) {return Number(num);}
                ).join (".");
            }
            document.location = clearNum (primaryValue) + "-" +
                clearNum (targetValue) + ".xml";
            return false;
        });
    }
)
</script>
<style>
html {
    color: #333;
    background-color: #09060d;
    padding: 2%;
    position: absolute;
    top: 0; bottom: 0; left: 0; right: 0;
    display: flex;
    overflow: hidden;
}
body {
    background-color: #7F8583;
    width: 60%;
    min-width: 38em;
    max-height: 96%;
    display: flex;
    margin: auto;
    padding: 1ex;
    text-align: center;
    font-family: 'Trebuchet MS', Helvetica, sans-serif;
    border-radius: 0.75ex;
}
div {
    background-color: #d1d3d2;
    padding: 1.5ex;
    display: flex;
    flex-flow: column;
    width: 100%;
}
h1 {font-family: Arial, Helvetica, sans-serif;}
h1+form {margin-top: 0;}
form {
    margin: 5%;
    display: flex;
    flex-flow: column;
    overflow-y: auto;
}
fieldset {border: none; overflow-y: auto;}
a {color: #333;}
form a {font-size: larger;}
fieldset p {
    text-align: right;
    width: 16em;
    margin-left: auto; margin-right: auto;
}
form + p, p + p {margin-top: 0;}
a:hover {text-decoration: none;}
.impossible {opacity: 0.33; filter: alpha(opacity=33);}
.hidden {visibility: hidden;}
</style>
<div>
    <h1>Ableton Live API Documentation</h1>
    <form>
        <fieldset>
'''

workdir = os.path.abspath (os.path.dirname (__file__))
is_source_xml = \
    lambda filename: re.compile('\d+\.\d+\.\d+\.xml').match (filename)
primary_filenames = [filename for filename in os.listdir (workdir)
    if is_source_xml (filename)]
fill_num = \
    lambda version: '.'.join ([num.zfill (2) for num in version.split('.')])
primary_filenames.sort(key=fill_num)
for i, filename in enumerate (reversed (primary_filenames)):
    version = filename.replace ('.xml', '')
    version_filled = fill_num (version)
    
    content += '            <p>\n                <a href="' + \
        filename + '">Live <strong>' + version + '</strong></a>\n'
    
    content += \
            '                <input type="radio" name="primary" value="' + \
        version_filled + '"'
    if i == 0: content += ' class="hidden"' # empty space the size of a radio button
    content += '>\n'
    
    content += \
            '                <input type="radio" name="target" value="' + \
        version_filled + '"'
    if i == len (primary_filenames) - 1: content += ' class="hidden"' # empty space the size of a radio button
    content += '>\n'

content += '''        </fieldset>
        <p><input type="submit" value="Compare" disabled>
    </form>
    <p>Thanks to <strong>Hanz Petrov</strong> for an
        <a href="https://github.com/NSUSpray/LiveAPI_MakeDoc">
            API_MakeDoc script</a>!
    <p>Thanks to <strong>Julien Bayle</strong> who published
        <a href="https://structure-void.com/ableton-live-midi-remote-scripts/#liveAPI">
            documentation for many versions of Live</a>!
    <p><a href="https://vk.com/nsu.spray">Vladimir Zevakhin</a>, 2016–2022
</div>
'''

with open ('index.html', 'w') as indexfile:
    indexfile.write (codecs.BOM_UTF8)
    indexfile.write (content)
