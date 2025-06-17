FROM python:3.12-slim-bullseye as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/source \
    LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry==1.7.1

RUN poetry --version > /tmp/poetry_version.txt && cat /tmp/poetry_version.txt

WORKDIR /source

COPY poetry.lock pyproject.toml ./

RUN poetry export --output requirements.txt --without-hashes --with-credentials --only main
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /source/wheels -r requirements.txt


FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/dist \
    LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8

WORKDIR /dist

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY --from=builder /source/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY apps ./apps
COPY manage.py ./manage.py
COPY settings.py ./settings.py
COPY yoyo.ini ./yoyo.ini
# COPY migrations ./migrations

CMD ["python", "manage.py"]
