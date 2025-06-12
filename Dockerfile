FROM python:3.13.3-alpine3.21
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "admin_run.py"]
