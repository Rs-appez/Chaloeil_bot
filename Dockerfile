FROM python:3.13-slim

ENV TZ="Europe/Brussels"

WORKDIR /chaloeil

COPY . /chaloeil/
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
