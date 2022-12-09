FROM python:3

RUN pip3 install numpy scipy matplotlib

RUN mkdir /tmp/matplotlib
RUN chmod 777 /tmp/matplotlib
ENV MPLCONFIGDIR=/tmp/matplotlib

WORKDIR /run
ENTRYPOINT python3 /run/main.py