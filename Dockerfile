FROM python:3.14-alpine

ENV TZ="Europe/Brussels"

WORKDIR /chaloeil

COPY requirements.txt /chaloeil/
RUN pip install -r requirements.txt

COPY . /chaloeil/

ENTRYPOINT ["python3", "main.py"]
