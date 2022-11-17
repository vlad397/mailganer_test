FROM python:2.7.15

WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn mail_system.wsgi:application --bind 0.0.0.0:8000