FROM python:3.8.12-slim-buster

COPY ./requirements.txt /bw-app/requirements.txt
WORKDIR /bw-app 
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
COPY . /bw-app

RUN echo $(whoami)
ENV PATH $PATH:$HOME/.local/bin
RUN pip install pipenv --user


CMD gunicorn -b 0.0.0.0:$PORT -w 4 app:beerwhisperer
