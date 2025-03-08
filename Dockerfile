FROM python:3.11

WORKDIR /localapp

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y libpq-dev gcc postgresql-client

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--pythonpath", "/", "localapp.wsgi:app"]
