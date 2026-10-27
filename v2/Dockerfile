FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY v2/app.py .

ENV PORT=5002
EXPOSE 5002

CMD ["python", "app.py"]
