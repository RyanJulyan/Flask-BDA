
FROM ubuntu:18.04

LABEL vendor="bda"
LABEL Created="{DeveloperName} <email@example.com>"
LABEL maintainer="{DeveloperName}"
LABEL version="0.0.0.1"
LABEL description="This is a default docker file for the bda system"

RUN apt-get update -y && apt-get install -y python-pip python3.8-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
ENTRYPOINT ["python", "./run.py"]
CMD [ "python", "./run.py" ]
