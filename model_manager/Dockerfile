FROM python:3.10.2

RUN mkdir -p modelmanager
COPY . /modelmanager

WORKDIR /modelmanager

RUN pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir -v

VOLUME /modelmanager

CMD python model_manager.py