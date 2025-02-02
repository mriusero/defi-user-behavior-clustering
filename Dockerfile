FROM python:3.11-slim

RUN useradd -m -u 1000 user

USER user

ENV PATH=$PATH:/home/user/.local/bin

WORKDIR /app
RUN ls -l /app


COPY --chown=user pyproject.toml uv.lock* /app/
RUN ls -l /app

RUN apt-get update && apt-get install -y tree
RUN tree /app

RUN pip install --upgrade pip \
    && pip install uv \
    && uv sync

COPY --chown=user . /app/

RUN apt-get update && apt-get install -y tree
RUN tree /app

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]