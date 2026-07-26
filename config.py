import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'trac-bsit-schedule-secret-2024')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'schedule.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BACKUP_DIR = os.path.join(BASE_DIR, 'instance', 'backups')
    # Desktop-only: no mobile support
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
