FROM python:3.6-stretch

RUN apt-get update \
    && pip install -U pip \
    && pip install pipenv awscli \
    && pip install ansible-vault

RUN pip install luigi boto3 pandas slackclient==2.0.0

WORKDIR $HOME/app

ENV PYTHONPATH=$HOME/app
ENV AWS_DEFAULT_REGION=ap-northeast-1

COPY . .
