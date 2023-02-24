FROM python:3.10.2

RUN mkdir -p modelserver
COPY . /modelserver

WORKDIR /modelserver

RUN pip install --upgrade pip

RUN pip install flask --no-cache-dir -v

RUN pip install numpy --no-cache-dir -v

RUN pip install tensorflow --no-cache-dir -v

RUN pip install scikit-learn --no-cache-dir -v

VOLUME /modelserver

CMD python mlp_model_serve.py