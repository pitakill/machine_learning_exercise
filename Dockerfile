FROM python:3.6
MAINTAINER Leopoldo Caballero <polo@pitakill.net>

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY api.py ./
COPY train.py ./
COPY intents.json ./

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python train.py

CMD [ "python", "./api.py" ]
