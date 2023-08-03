FROM python:3.10

WORKDIR opt/src/

COPY ./requirements.txt /opt/src/requirements.txt

RUN apt-get update

RUN pip3 install --no-cache-dir --upgrade -r /opt/src/requirements.txt

COPY ./app /opt/src/app/
COPY ./alembic ./alembic/
COPY ./include ./include/
COPY ./.gitignore .
COPY ./alembic.ini .
COPY ./.env .

#COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]