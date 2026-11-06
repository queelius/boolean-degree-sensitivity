FROM python@sha256:019e31cc1f52e4139d338bca44f27b71339a9da261738fd80fab9cf4595152fc
ENV OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt /requirements.txt
# pynauty 2.8.8.1 builds nauty from source; the compiler is removed after installation
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
 && python -m pip install --no-cache-dir -r /requirements.txt \
 && apt-get purge -y build-essential && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
