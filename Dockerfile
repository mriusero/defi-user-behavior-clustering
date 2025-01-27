FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock* /app/

RUN pip install --upgrade pip \
    && pip install uv \
    && uv sync

COPY . /app/

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]