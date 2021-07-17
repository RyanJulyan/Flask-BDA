
# FROM ubuntu:latest

# Alpine is meant to be much smaller
# FROM alpine:latest

# Alpine is suposed to be slow to build and actually can result in larger image sizes: https://pythonspeed.com/articles/alpine-docker-python/
FROM python:3.8-slim

LABEL vendor="fllask-bda"
LABEL Created="{DeveloperName} <email@example.com>"
LABEL maintainer="{DeveloperName}"
LABEL version="0.0.0.1"
LABEL description="This is a default docker file for the flask-bda system"

# for Ubuntu
# RUN apt-get update -y && apt-get install -y python3-pip python3.8-dev -y --no-install-recommends

# for Alpine
# RUN apk add --no-cache python3-dev && apk add --update py-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["run.py" ]
