FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
CMD ["python", "app/extract_outline.py"]