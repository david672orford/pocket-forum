# https://hub.docker.com/_/python
FROM python:3.14-alpine3.23
LABEL org.opencontainers.image.authors="David Chappell <David.Chappell@trincoll.edu>"
ARG uid
COPY requirements.txt /tmp/requirements.txt
RUN apk add --no-cache git libspatialite \
	&& pip3 install -r /tmp/requirements.txt \
	&& adduser -u $uid -G users -D app
WORKDIR /app
COPY . .
EXPOSE 5000
USER app
#CMD ["python", "start.py"]
CMD ["gunicorn", "--workers=1", "--threads=4", "--bind=:5000", "--access-logfile=-", "app.production:app"]
