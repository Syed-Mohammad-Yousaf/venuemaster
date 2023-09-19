FROM python:3.10.12-slim-buster as base

FROM base as builder

RUN apt-get update && apt-get install -y \
    gcc \
    git \
    libpq-dev \
    postgresql-client \
    binutils \
    libproj-dev \
    gdal-bin \
    python-lxml \
    libcairo2 \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN pip install pip


WORKDIR /install

FROM builder as dev
WORKDIR /opt/venuemaster
COPY requirements/dev.txt requirements/dev.txt
RUN pip install -r requirements/dev.txt
COPY . ./

FROM builder as prod_builder
COPY requirements/prod.txt /prod.txt
RUN pip install --prefix=/install --no-warn-script-location -r /prod.txt

FROM base as prod
RUN apt update && apt install -y \
    postgresql-client \
    binutils \
    libproj-dev \
    gdal-bin \
    python-lxml \
    libcairo2 \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev

COPY --from=prod_builder /install /usr/local
WORKDIR /opt/venuemaster
COPY . ./
EXPOSE 8000
