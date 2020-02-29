FROM python:3.7
RUN mkdir /root/BaseQuery
COPY . /root/BaseQuery
RUN cd /root/BaseQuery && ./install.sh
