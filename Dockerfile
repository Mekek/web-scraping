# Используем официальный образ Python в качестве базового
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все необходимые файлы в контейнер
COPY . .

# Устанавливаем необходимые зависимости (если есть)
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем скрипты с задержкой в 1 секунду между ними
CMD ["bash", "-c", "python scrapping.py && sleep 1 && python comparison.py && sleep 1 && python extracting_legal_entities.py && sleep 1 && python extracting_natural_persons.py"]
