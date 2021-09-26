FROM python:3.8-slim

RUN pip install --upgrade pip

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

WORKDIR /souzashopbot

COPY *.py /souzashopbot/

CMD python bot.py