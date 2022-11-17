FROM python:3.10.4

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn mail_system.wsgi:application --bind 0.0.0.0:8000