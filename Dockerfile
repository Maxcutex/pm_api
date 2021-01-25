FROM python:3.8.7-buster
WORKDIR /usr/src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST 0.0.0.0
RUN apt-get update && apt-get install -y postgresql gcc python3-dev musl-dev build-essential libssl-dev libffi-dev
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /usr/src/postgres-data
COPY . /usr/src
EXPOSE 5000
CMD ["python", "run.py", "runserver", "--host=0.0.0.0"]
