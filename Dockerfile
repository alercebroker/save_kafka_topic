FROM rappdw/docker-java-python

COPY . /app

RUN pip3 install --upgrade awscli 
RUN  pip3 install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

CMD ["python3", "scripts/service.py", "config.json"]
