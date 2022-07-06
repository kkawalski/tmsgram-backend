FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get -y update && apt-get -y install netcat \
&& apt-get install gcc -y \
&& apt-get clean



WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip & pip install -r requirements.txt

COPY . .
RUN ls /app

ENTRYPOINT ["/app/entrypoint.sh"]
