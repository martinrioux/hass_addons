# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
FROM python:3.9-alpine3.16

RUN apk add --no-cache alsa-lib sdl2-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mqtt_soundboard.py ./

CMD [ "python", "./mqtt_soundboard.py" ]
