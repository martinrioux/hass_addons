# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
FROM python:alpine3.17

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mqtt_soundboard.py ./

CMD [ "python", "./mqtt_soundboard.py" ]
