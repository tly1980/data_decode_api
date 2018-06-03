FROM python:3.6-alpine3.7
COPY . /app
WORKDIR /app
RUN apk add --no-cache --virtual .build-deps \
  gcc \
  musl-dev \
  && pip install -r requirements.txt \
  && apk del .build-deps
CMD ["gunicorn", "-w 4", "app:app", "-b :80"]
