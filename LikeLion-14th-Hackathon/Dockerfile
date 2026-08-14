# Dockerfile

FROM python:3.11-slim

# 파이썬 로그가 버퍼링 없이 바로 출력되게 설정
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 의존성 먼저 설치 (빌드 캐시 활용을 위해 코드보다 먼저 복사)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 코드 전체 복사 (main.py, felix.py, emil.py, johannes.py, klara.py 등)
COPY . .

EXPOSE 8000

# $PORT 환경변수가 있으면 그걸 쓰고 (Render 등 배포 플랫폼용), 없으면 8000번 기본값
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
