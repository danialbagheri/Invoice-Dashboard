FROM ubuntu:16.04
#Flushing the STDIN and STDOUT buffer
#ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
apt-get upgrade -y && \
apt-get dist-upgrade -y && \
apt-get install -y --no-install-recommends \
	python2.7 \
	python-pip \
	libssl-dev \
	libapache2-mod-wsgi \
	python-mysqldb \
	libmysqlclient-dev \
	&& apt-get update -y \
	&& pip install --upgrade setuptools \
	&& pip install mysqlclient \
	&& rm -rf /var/lib/apt/lists/*

RUN mkdir /var/www/
WORKDIR /var/www/
ADD requirements.txt /var/www/

RUN pip install -r requirements.txt
COPY . /var/www/

RUN pip install virtualenv
WORKDIR /var/www/linco/
RUN ["/bin/bash", "-c", "python manage.py makemigrations && python manage.py migrate"] 

