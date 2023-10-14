FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install python3 gcc vim curl zsh git g++ libmysqlclient-dev mysql-server libcurl4-openssl-dev -y
RUN apt install python3-pip -y
RUN pip3 install requests flask flask_mysqldb

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"