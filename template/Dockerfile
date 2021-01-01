
# FROM ubuntu:18.04

# Alpine is meant to be much smaller
FROM alpine:latest

LABEL vendor="bda"
LABEL Created="{DeveloperName} <email@example.com>"
LABEL maintainer="{DeveloperName}"
LABEL version="0.0.0.1"
LABEL description="This is a default docker file for the bda system"

# for Ubuntu
# RUN apt-get update -y && apt-get install -y python-pip python3.8-dev

# for Alpine
RUN apk add --no-cache python3-dev && apk add --update py-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["run.py" ]
