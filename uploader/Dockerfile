FROM python:3.9-slim

WORKDIR /app

RUN pip install flask flask-cors minio requests

COPY uploader.py .

EXPOSE 8081

CMD ["python", "uploader.py"]
