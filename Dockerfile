FROM python:3.7

COPY . /app
RUN  pip install --no-cache-dir -r ./requirements.txt
WORKDIR /app

CMD["python", "scripts/service.py", "config.json"]
