FROM python:3.6

ADD ./requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt
COPY . /app
WORKDIR /app

ENV ENV="PROD"
ENV DEBUG=false
ENV FLASK_DEBUG=false

EXPOSE 7465
EXPOSE 5000
EXPOSE 27017

CMD gunicorn -b 0.0.0.0:7465 main:app
