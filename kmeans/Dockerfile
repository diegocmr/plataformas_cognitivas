FROM python:3.10.2

RUN mkdir -p modelserver
COPY . /modelserver

WORKDIR /modelserver

RUN pip install -r requirements.txt -v

VOLUME /modelserver

CMD python kmeans_model_serve.py