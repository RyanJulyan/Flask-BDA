
# Alpine is suposed to be slow to build and actually can result in larger image sizes: https://pythonspeed.com/articles/alpine-docker-python/
FROM python:3.8-slim

LABEL vendor="Fllask-BDA"
LABEL Created="{DeveloperName} <email@example.com>"
LABEL maintainer="{DeveloperName}"
LABEL version="0.0.1"
LABEL description="This is a default docker file for the Flask-BDA system"

# install FreeTDS and dependencies
RUN apt-get update \
    && apt-get install unixodbc -y \
    && apt-get install unixodbc-dev -y \
    && apt-get install freetds-dev -y \
    && apt-get install freetds-bin -y \
    && apt-get install tdsodbc -y \
    && apt-get install --reinstall build-essential -y

# populate "ocbcinst.ini"
RUN echo "[FreeTDS]\n\
    Description = FreeTDS unixODBC Driver\n\
    Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
    Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["run.py" ]
