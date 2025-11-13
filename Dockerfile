FROM python:3.10-slim

# Python 환경 변수 설정
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 비root 사용자 생성
RUN useradd -m -u 1000 appuser

WORKDIR /app

# 의존성 설치 (root 권한 필요)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY --chown=appuser:appuser ./src .

# 비root 사용자로 전환
USER appuser

CMD ["python", "cmake_mcp_main.py"]