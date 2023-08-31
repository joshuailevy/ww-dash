FROM continuumio/miniconda3

COPY requirements.txt /tmp/
COPY ./app /app
WORKDIR "/app"

RUN pip install -r ../tmp/requirements.txt
EXPOSE 8050
CMD [ "gunicorn", "--workers=4", "--threads=1", "-b :8050", "app:server"]
