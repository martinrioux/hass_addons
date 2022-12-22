# Home Assistant Python MQTT Soundboard

Used to start, pause, loop and stop music and soundfx from Home Assistant dashboards using MQTT commands.

# Topics
## soundboard/music
Payload can be:
filename.ext    Plays the <filename.ext> as music
loop_on         Enables looping. Must be set BEFORE playing the music
loop_off        Disables looping. Must be set BEFORE playing the music
fadeout[,XX]    Fades out the current running music. You can do fadeout,1000 to fadeout over 1000ms
pause           Pause the music
play            Play the music
stop            Stops the music and all still running sound effects

## soundboard/sound
Payload can be:
filename.ext    Plays the <filename.ext> as sound effect

## soundboard/volume
Payload can be:
+XX     Increase volume of XX percent
-XX     Decrease volume of XX percent
XX      Set volume to XX percent