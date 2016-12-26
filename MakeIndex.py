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
        $submit.attr ("value", "Get Comparison");
        $submit.removeAttr ("disabled");
    } else {
        $submit.attr ("value", "Check for Comparison");
        $submit.attr ("disabled", true);
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
body {
    padding: 3%;
    text-align: center;
    font-family: 'Trebuchet MS', Helvetica, sans-serif;
}
h1 {font-family: Arial, Helvetica, sans-serif; color: #333;}
form a {font-size: larger;}
a:hover {text-decoration: none;}
.hidden {visibility: hidden;}
</style>
    </head>
    <body>
        <h1>Ableton Live API Documentation</h1>
        <form>
'''

workdir = os.path.abspath (os.path.dirname (__file__))
primary_filenames = [filename for filename in os.listdir (workdir) if re.compile('\d+\.\d+\.\d+\.xml').match (filename)]
for i, filename in enumerate (primary_filenames):
    version = filename.replace ('.xml', '')
    content += '            <p><a href="' + filename + '">Version <strong>' + version + '</strong></a> '
    content += '<input type="radio" name="primary" value="' + version + '"'
    if i == len (primary_filenames) - 1: content += ' class="hidden"'
    content += '> <input type="radio" name="target" value="' + version + '"'
    if i == 0: content += ' class="hidden"'
    content += '></p>\n'

content += '''            <p><input type="submit" value="Check for Comparison" disabled></p>
            </form>
        <p>Thanks to <strong>Hanz Petrov</strong> for an <a href="http://remotescripts.blogspot.ru/p/support-files.html">API_MakeDoc script</a>!</p>
        <p>Thanks to <strong>Julien Bayle</strong> who published <a href="http://julienbayle.net/ableton-live-9-midi-remote-scripts/">documentation for many versions of Live</a>!</p>
        <p><a href="https://vk.com/nsu.spray">Vladimir Zevakhin</a>, 2016</p>
    </body>
</html>
'''

with open ('index.html', 'w') as indexfile:
    indexfile.write (codecs.BOM_UTF8)
    indexfile.write (content)
