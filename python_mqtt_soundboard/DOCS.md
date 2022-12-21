# Python MQTT Soundboard

## Topic -> payload format
soundboard/<soundfilename.ext> -> "<options>"
soundboard/volume -> [+<value>, -<value> or <value> to set]

## Options
If empty, plays normaly and stop
"loop" -> Loop the sound effect
"stop" -> stops the sound effect
