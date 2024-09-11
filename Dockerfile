FROM python:alpine

COPY pyproject.toml pdm.lock README.md /app/
COPY src /app/src

WORKDIR /app
RUN pip install -e . --no-cache-dir

ENV HOST=0.0.0.0 \
    PORT=1337

CMD ["/bin/sh", "-c", "exec python -m echo_test $HOST $PORT"]