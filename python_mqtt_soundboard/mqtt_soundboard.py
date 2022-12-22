
import os
from pygame import mixer
from pygame import error as pygame_error
from paho.mqtt import client as mqtt_client
import time
import ujson
import logging

with open("/data/options.json", "r") as f:
    options = f.read()
config = ujson.loads(options)

mqtt_host = config.get('mqtt_host')
mqtt_port = int(config.get('mqtt_port'))
mqtt_username = config.get('mqtt_username')
mqtt_password = config.get('mqtt_password')

mixer.init()

media_folder = "/media/"

logging.info("Python MQTT Soundboard starting")

class MQTTSoundboard:
    def __init__(self):
        self.mqtt = None
        self.subscribed_topic = ["soundboard/#"]
        self.sounds = {}
        self.volume = 0.5
        self.loop_music = False

    def start(self):
        self.connect_mqtt()

    def connect_mqtt(self):
        self.mqtt = mqtt_client.Client()
        self.mqtt.username_pw_set(mqtt_username, mqtt_password)
        self.mqtt.on_connect = self._on_connect
        self.mqtt.on_disconnect = self._on_disconnect
        self.mqtt.message_callback_add("soundboard/music", self.music_callback)
        self.mqtt.message_callback_add("soundboard/sound", self.sound_callback)
        self.mqtt.message_callback_add("soundboard/volume", self.volume_callback)
        self.mqtt.connect_async(mqtt_host, mqtt_port)
        self.mqtt.loop_forever()

    def _on_connect(self, client, userdata, flags, rc):
        for topic in self.subscribed_topic:
            self.mqtt.subscribe(topic, qos=0)

    def _on_disconnect(self, client, userdata, rc):
        """MQTT Disconnect callback."""
        logging.error("Python MQTT Soundboard lost MQTT connection")
        self.mqtt.loop_stop()

    def _on_message(self, client, userdata, message):
        pass

    def music_callback(self, client, userdata, message):
        payload: str = message.payload.decode("UTF-8", "ignore")
        args = payload.split(",")
        # FADEOUT
        if args[0] == "fadeout":
            try:
                delay = int(args[1])
            except (TypeError, IndexError):
                delay = 3
            for sound in self.sounds:
                self.sounds[sound].stop()
            mixer.music.fadeout(delay)
        # STOP
        elif args[0] == "stop":
            for sound in self.sounds:
                self.sounds[sound].stop()
            mixer.music.stop()
        # PAUSE
        elif args[0] == "pause":
            mixer.music.pause()
        # START
        elif args[0] == "play":
            try:
                if self.loop_music:
                    mixer.music.play(-1)
                else:
                    mixer.music.play()
            except pygame_error:
                pass
        # ENABLE MUSIC LOOP
        elif args[0] == "loop_on":
            self.loop_music = True
        # DISABLE MUSIC LOOP
        elif args[0] == "loop_off":
            self.loop_music = False
        # PLAY NEW MUSIC
        else:
            mixer.music.stop()
            file = f"{media_folder}{args[0]}"
            if not os.path.exists(file):
                logging.error(f"Music file '{file}' not found")
                return
            mixer.music.load(file)
            mixer.music.set_volume(self.volume)
            if self.loop_music:
                mixer.music.play(loops=-1, start=0.0, fade_ms=1500)
            else:
                mixer.music.play()

    def sound_callback(self, client, userdata, message):
        payload: str = message.payload.decode("UTF-8", "ignore")
        args = payload.split(",")

        if args[0] not in self.sounds:
            file = f"{media_folder}{args[0]}"
            if not os.path.exists(file):
                logging.error(f"Sound file '{file}' not found")
                return
            self.sounds[args[0]] = mixer.Sound(file)
        else:
            self.sounds[payload].stop()
        self.sounds[payload].set_volume(self.volume)
        self.sounds[payload].play()

    def volume_callback(self, client, userdata, message):
        payload: str = message.payload.decode("UTF-8", "ignore")
        try:
            if payload.startswith("+"):
                self.volume += int(payload[1:])/100
            elif payload.startswith("-"):
                self.volume -= int(payload[1:])/100
            else:
                self.volume = int(payload)/100
        except ValueError:
            pass

        if self.volume < 0:
            self.volume = 0
        elif self.volume > 1:
            self.volume = 1
        logging.info(f"New volume: {self.volume}")
        mixer.music.set_volume(self.volume)
        for sound in self.sounds:
            self.sounds[sound].set_volume(self.volume)


if __name__ == "__main__":
    app = MQTTSoundboard()
    while True:
        app.start()
        logging.error("Python MQTT Soundboard stopped and will restart")
