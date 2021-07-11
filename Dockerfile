FROM python:3

WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get install -y netcat && chmod 777 /code && useradd -ms /bin/bash eblackbu

USER eblackbu
RUN pip install -r requirements.txt && mkdir -p /home/eblackbu/.local/logs

COPY . /code/
