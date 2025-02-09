# BASE IMAGE
FROM python:3.11-slim


WORKDIR /app


COPY requirements.txt ./

# Kütüphaneleri yükle
RUN apt-get update \
    && apt-get install -y curl libgl1-mesa-glx libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt


COPY assets ./assets
COPY elbow_plots ./elbow_plots
COPY cluster_plots ./cluster_plots
COPY app.py ./
COPY medium_model.pt ./
COPY . ./

# Healthcheck 
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Çalıştır
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
