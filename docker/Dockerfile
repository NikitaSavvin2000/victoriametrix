FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml pdm.lock /app/

COPY docker-entrypoint.sh /usr/local/bin/

RUN pip install pdm && pdm install --no-lock

COPY . /app/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
