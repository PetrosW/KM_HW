FROM python:3.7.10-slim-buster

COPY requirements* /

RUN apt-get update && \
    cat requirements.apt | xargs apt-get install -y && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY color_avg_computer.py /

CMD ["/color_avg_computer.py"]