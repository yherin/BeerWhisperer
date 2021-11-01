FROM python:3.8.12-slim-buster

COPY ./requirements.txt /bw-app/requirements.txt
WORKDIR /bw-app
RUN apt-get -y update && apt-get install -y libzbar-dev ffmpeg libsm6 libxext6 
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
COPY . /bw-app

RUN echo $(whoami)
ENV PATH $PATH:$HOME/.local/bin
RUN pip install pipenv --user


CMD gunicorn -b 0.0.0.0:8000 -w 4 app:beerwhisperer
