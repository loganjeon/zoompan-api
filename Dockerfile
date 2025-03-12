FROM python:3.13.2-slim-bookworm

# FFmpeg 설치
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 필요한 파일 복사
COPY ./app/requirements.txt /app/requirements.txt

# 의존성 설치
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 애플리케이션 코드 복사
COPY ./app /app

# 포트 노출
EXPOSE 80

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

