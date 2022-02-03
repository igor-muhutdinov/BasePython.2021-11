# Запустить контейнер командой:
# docker run -p 8000:8000 app

# Исходный образ
FROM python:3.9-buster

# Рабочая директория
WORKDIR /app

# Установка зависимостей
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# Копируем данные приложения
COPY ./app .

# Информируем о номер используемого порта
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]