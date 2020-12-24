FROM python:3.7-alpine
WORKDIR /usr/src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /usr/src/postgres-data
COPY . /usr/src
EXPOSE 5000
CMD ["python", "run.py", "runserver"]
