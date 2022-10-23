import os
from dotenv import load_dotenv


# Получение пути до файла с переменными
DOTENV_PATH = os.path.join(os.path.dirname(
    __file__), '.env').replace('\\', '/')

print(DOTENV_PATH)

if os.path.exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)

print("==================================================")
print(f"Работа идет на {os.getenv(key='Postgrsql')} базе!")
print("==================================================\n")

# Настройки базы данных
DATABASE = {
    'engine': os.getenv(key='POSTGRES_ENGINE'),
    'db': os.getenv(key='POSTGRES_DB'),
    'user': os.getenv(key='POSTGRES_USER'),
    'password': os.getenv(key='POSTGRES_PASSWORD'),
    'host': os.getenv(key='POSTGRES_HOST'),
    'port': os.getenv(key='POSTGRES_PORT'),
}