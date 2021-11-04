FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

# Install system requirements
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends  \
    build-essential gettext libpq-dev git python3-dev poppler-utils binutils libproj-dev gdal-bin \
 && apt-get autoremove -y \
 && apt-get clean -y

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt
