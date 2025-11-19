FROM python:3.13-alpine

ENV TZ="Europe/Brussels"

WORKDIR /chaloeil

COPY . /chaloeil/
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
