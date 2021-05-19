FROM python:3.7.10-slim-buster

COPY requirements* /

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY image_reader.py /

CMD ["/image_reader.py"]