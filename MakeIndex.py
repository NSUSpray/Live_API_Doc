# -*- coding: utf-8 -*-
import sys, os, codecs, re

reload (sys)
sys.setdefaultencoding ('utf-8')


content = ''
content += '''<!DOCTYPE html>
<html>
    <head>
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
            document.location =
                $("[name='primary']:checked").val () + "-"
                + $("[name='target']:checked").val () + ".xml";
            return false;
        });
    }
)
        </script>
        <style>
html {color: #333; background-color: #09060d;}
body {
    background-color: #7F8583;
    margin: 2% 20%;
    padding: 1ex;
    text-align: center;
    font-family: 'Trebuchet MS', Helvetica, sans-serif;
    border-radius: 0.75ex;
}
div {background-color: #d1d3d2; padding: 1.5ex;}
h1 {font-family: Arial, Helvetica, sans-serif;}
h1+form {margin-top: 0;}
form {margin: 5%;}
fieldset {
    border: none;
    max-height: 20em;
    overflow-y: auto;
}
a {color: #333;}
form a {font-size: larger;}
a:hover {text-decoration: none;}
.impossible {opacity: 0.33; filter: alpha(opacity=33);}
.hidden {visibility: hidden;}
</style>
    </head>
    <body><div>
        <h1>Ableton Live API Documentation</h1>
        <form>
            <fieldset>
'''

workdir = os.path.abspath (os.path.dirname (__file__))
filenames = reversed (os.listdir (workdir))
is_source_xml = lambda filename: re.compile('\d+\.\d+\.\d+\.xml').match (filename)
primary_filenames = [filename for filename in filenames if is_source_xml (filename)]
for i, filename in enumerate (primary_filenames):
    version = filename.replace ('.xml', '')
    
    content += '                <p><a href="' + filename + '">Version <strong>' + version + '</strong></a> '
    
    content += '<input type="radio" name="primary" value="' + version + '"'
    if i == 0: content += ' class="hidden"' # пустое место размером с радиокнопку
    content += '>'
    
    content += ' <input type="radio" name="target" value="' + version + '"'
    if i == len (primary_filenames) - 1: content += ' class="hidden"' # пустое место размером с радиокнопку
    content += '></p>\n'

content += '''                </fieldset>
                <p><input type="submit" value="Compare" disabled></p>
            </form>
        <p>Thanks to <strong>Hanz Petrov</strong> for an <a href="http://remotescripts.blogspot.ru/p/support-files.html">API_MakeDoc script</a>!</p>
        <p>Thanks to <strong>Julien Bayle</strong> who published <a href="http://julienbayle.net/ableton-live-9-midi-remote-scripts/">documentation for many versions of Live</a>!</p>
        <p><a href="https://vk.com/nsu.spray">Vladimir Zevakhin</a>, 2016</p>
    </div></body>
</html>
'''

with open ('index.html', 'w') as indexfile:
    indexfile.write (codecs.BOM_UTF8)
    indexfile.write (content)
