FROM python:3.9-slim

WORKDIR /app

RUN pip install flask flask-cors pyjwt

COPY security.py .

EXPOSE 8080

CMD ["python", "security.py"]
