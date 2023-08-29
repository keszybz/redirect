#!/bin/bash
echo 'Content-type: text/html'
echo ''
echo '<html>'
echo '<head>'
echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
echo '<title>Gotcha</title>'
echo '<style>'
echo 'html { font-size: xx-large; }'
echo '</style>'
echo '</head>'
echo '<body>'
echo 'GOTCHA!'
echo '</body>'
echo '</html>'
mpv ./police.opus >& /dev/null &

