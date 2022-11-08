FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /DjangoFP

COPY Pipfile Pipfile.lock /DjangoFP/
RUN apk update && apk upgrade && \
    pip install pipenv && pipenv install --system \
    pipenv install -r requirements.txt

COPY . /DjangoFP/
