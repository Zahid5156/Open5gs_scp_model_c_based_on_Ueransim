FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ue_manager.py /app/
COPY ../../docker-compose.yml /app/
COPY configs /app/configs/

CMD ["tail", "-f", "/dev/null"]