from flask import Flask, request, jsonify
import uuid
import requests
from minio import Minio
import io
import hashlib
from datetime import datetime
import os

app = Flask(__name__)

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost')
MINIO_PORT = os.getenv('MINIO_PORT', '9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin123')

# Инициализация MinIO клиента
minio_client = Minio(
    f"{MINIO_ENDPOINT}:{MINIO_PORT}",
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

@app.route('/v1/upload', methods=['POST'])
def upload_file():
    # Проверка авторизации
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'No authorization header'}), 401
    
    # Получаем данные файла
    file_data = request.data
    if not file_data:
        return jsonify({'error': 'No file data'}), 400
    
    # Имитация обработки/сжатия изображения
    # В реальном приложении здесь была бы логика сжатия
    processed_data = file_data  # Заглушка
    
    # Генерируем имя файла
    filename = f"{uuid.uuid4()}.jpg"
    
    # Сохраняем в MinIO
    try:
        # Загружаем файл в бакет 'images'
        minio_client.put_object(
            bucket_name='images',
            object_name=filename,
            data=io.BytesIO(processed_data),
            length=len(processed_data),
            content_type='image/jpeg'
        )
        
        return jsonify({
            'filename': filename,
            'size': len(processed_data),
            'url': f'/v1/user/{filename}'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
