# Используем официальный образ Python 3.8 как базовый образ
FROM python:3.8

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы зависимостей и код в контейнер
COPY requirements.txt requirements.txt
COPY app.py app.py

# Устанавливаем зависимости из requirements.txt
RUN pip install -r requirements.txt

# Открываем порт, на котором будет работать приложение в контейнере
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]
