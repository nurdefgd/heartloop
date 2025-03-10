import os
import subprocess
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def backup_database():
    try:
        # Получаем переменные окружения
        db_url = os.environ.get('DATABASE_URL')
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        s3_bucket = os.environ.get('S3_BACKUP_BUCKET')

        if not all([db_url, aws_access_key, aws_secret_key, s3_bucket]):
            raise ValueError("Missing required environment variables")

        # Создаем имя файла для бэкапа
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_{timestamp}.sql'

        # Создаем бэкап базы данных
        logger.info("Starting database backup...")
        subprocess.run([
            'pg_dump',
            db_url,
            '-f', backup_file
        ], check=True)

        # Загружаем бэкап в S3
        logger.info("Uploading backup to S3...")
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )

        s3_client.upload_file(
            backup_file,
            s3_bucket,
            f'backups/{backup_file}'
        )

        # Удаляем локальный файл бэкапа
        os.remove(backup_file)
        logger.info("Backup completed successfully!")

    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        raise

if __name__ == '__main__':
    backup_database() 