FROM python:3.8-slim

WORKDIR /app

COPY Adarsh /app/Adarsh


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "-m", "Adarsh"]
