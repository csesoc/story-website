## BASE BUILD THAT BOTH DEV AND PROD INHERIT FROM

# pull official base image
FROM python:3.8.10-slim-buster AS base

# set work directory
WORKDIR /backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile* /backend/

RUN pip install pipenv

EXPOSE 5001

## DEV BUILD

FROM base as dev

RUN pipenv lock --dev --requirements > requirements.txt \
    && pip uninstall --yes pipenv \
    && pip install -r requirements.txt

CMD [ "python", "app.py" ]

## PROD BUILD

FROM base as prod

RUN pipenv lock --requirements > requirements.txt \
    && pip uninstall --yes pipenv \
    && pip install -r requirements.txt

CMD [ "gunicorn", "--bind", "0.0.0.0:5001", "app:app" ]
