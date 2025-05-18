FROM python:3.9-slim as builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/bin/ffmpeg /usr/bin/ffmpeg

WORKDIR /app
COPY . .
ENV PATH=/root/.local/bin:$PATH

CMD ["python", "main.py"]
