FROM python:3.10.2

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install nano

RUN mkdir -p modelserver
COPY . /modelserver

WORKDIR /modelserver

RUN pip install -r requirements.txt

VOLUME /modelserver

CMD python mlp_model_serve.py