FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home appuser
COPY app ./app
COPY model ./model
USER appuser
EXPOSE 8080
CMD ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "8080"]
