FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt-get update && apt-get install -y bash g++ libgl1-mesa-glx

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

COPY ./requirements.txt /var/www/requirements.txt
COPY . /app

RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r /var/www/requirements.txt