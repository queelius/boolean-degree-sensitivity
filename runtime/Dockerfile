FROM python@sha256:6ff506466f8b1e981719b468cc0023b8ef000b983cdec0eafe119d01f379e31d
ENV OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt /requirements.txt
RUN python -m pip install --no-cache-dir -r /requirements.txt
