FROM ubuntu:latest
MAINTAINER Federico Lopez Gomez "fico89@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libxml2-dev libxslt1-dev zlib1g-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["run.py"]