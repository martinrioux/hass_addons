# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
FROM python:3.9-bullseye

RUN apt-get update
RUN apt-get install -y libasound2-plugins

WORKDIR /usr/src/app

RUN pip install --no-cache-dir pygame paho-mqtt

COPY mqtt_soundboard.py ./

CMD [ "python", "./mqtt_soundboard.py" ]
