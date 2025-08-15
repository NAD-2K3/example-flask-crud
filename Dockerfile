FROM python:3.11.13-alpine3.22

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

RUN flask db init && \
    flask db migrate -m "entries table" && \
    flask db upgrade

EXPOSE 5000

ENTRYPOINT ["flask","run", "--host=0.0.0.0"]