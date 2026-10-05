FROM python:3.11-slim

# Metadatalar
LABEL maintainer="KidsVidEdu Team"
LABEL description="KidsVidEdu - AI Educational Video Studio for Children"

WORKDIR /app

# Tizim paketlari
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python paketlarini o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini nusxalash
COPY . .

# Python yo'li va sozlamalari
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1

# Xavfsizlik uchun maxsus portni ochamiz
EXPOSE 8000

# Serverni ishga tushirish (Uvicorn)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
