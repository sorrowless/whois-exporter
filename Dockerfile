FROM python:3.10 as build
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt
RUN apt update -y && apt install -y whois
COPY . .
EXPOSE 8000

WORKDIR /app/whois_exporter
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
