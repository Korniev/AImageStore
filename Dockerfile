# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/* /root/.cache

# Stage 2: Final image
FROM python:3.11-slim

WORKDIR /code

# Копіювання встановлених пакетів з builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Копіювання коду проекту
COPY . /code

# Встановлення секретного ключа
ENV SECRET_KEY "CLyofVvfzVhdfAlRrMn2OZ53Oi3aIJlPdZrfIqZgau5Puc9qRp"

# Встановлення Gunicorn
RUN pip install gunicorn

# Збір статичних файлів з правильним робочим каталогом
WORKDIR /code/aimagestore
RUN python manage.py collectstatic --noinput

# Відкриття порту
EXPOSE 8000

# Запуск Gunicorn з використанням WSGI
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "aimagestore.wsgi:application"]

