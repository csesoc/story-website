# pull official base image
FROM python:3.10.3-slim-buster

# set work directory
WORKDIR /backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile* /backend/

RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pip uninstall --yes pipenv
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "app.py" ]
