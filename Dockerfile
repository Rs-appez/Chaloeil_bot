FROM python:3.13.3-slim

ENV TZ="Europe/Brussels"

RUN apt-get update && apt-get install -y 

WORKDIR /chaloeil


COPY requirements.txt /chaloeil/
RUN pip install -r requirements.txt

COPY . /chaloeil/
CMD python main.py
