FROM apache/airflow:2.9.3

ENV AIRFLOW_HOME=/opt/airflow

USER root

RUN apt-get update && apt-get install -y python3-pip \
    libcurl4-gnutls-dev \
    librtmp-dev \
    python3-dev \
    libpq-dev \
    inotify-tools

# COPY ./config/* /config/

# RUN chmod +x -R /config

COPY requirements.txt requirements.txt

USER airflow

RUN pip install -U -r requirements.txt

EXPOSE 8080

WORKDIR ${AIRFLOW_HOME}
