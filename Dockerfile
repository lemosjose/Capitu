FROM python:3.12-slim AS bot 

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED=1 

COPY application /application 

WORKDIR /application

RUN apt update 
RUN apt install -y python3 python3-pip build-essential python3-venv


RUN pip3 install -r /application/requirements.txt

CMD python /application/src/main.py




