# Telegram bot with Django, pyTelegramBotAPI.

Телеграм бот, для регистрации пользователей в django, и записи на услугу.


## Для запуска бота:

 1. Скопируйте репозиторий, установите зависимости  `pip install -r requirements.txt`.
 2. Создайте файл `.env`, задайте переменные как в примере  - `.env_example`.
 3. Примените миграции `python3 manage.py migrate` и используйте команду:
 
        python run_polling.py
