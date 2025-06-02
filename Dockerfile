# Python 3.10.8 베이스 이미지 사용
FROM python:3.10.8-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 후 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY main.py .

# FastAPI 앱 실행 (uvicorn 사용)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
