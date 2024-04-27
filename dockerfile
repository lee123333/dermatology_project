FROM python:3.10.12

LABEL maintainer="leehaohsiang"
LABEL version="1.0"
LABEL description="winter final project to cosbi"

ENV PYTHONUNBUFFERED 1

RUN mkdir /skin_web
WORKDIR /skin_web
COPY . /skin_web/

RUN pip install -r requirements.txt

# Install vim
RUN apt-get update && apt-get install -y vim

# Start the Django development server
# CMD python3 manage.py runserver 0.0.0.0:1011
