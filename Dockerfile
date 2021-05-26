FROM ubuntu:20.04

WORKDIR /build

COPY . /build

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

RUN chmod a+x ./run.py

CMD [ "python3", "run.py" ]

