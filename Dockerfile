FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install --with-deps chromium

COPY . .

EXPOSE 5000

CMD ["sh", "-c", "flask --app run.py db upgrade && gunicorn -b 0.0.0.0:5000 run:app"]