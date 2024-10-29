import pandas as pd
import openai
from collections import Counter
import csv
import json


# Загрузка конфигурации из JSON-файла
with open("config.json") as config_file:
    config = json.load(config_file)

# Загрузка данных
df = pd.read_csv("data/compared_data.csv")

# Определение списка ключевых слов для юридических лиц
legal_entities = ["LLC", "LTD", "INC", "TR"]

# Фильтрация физических лиц
pre_individuals_df = df[~df["Owner Name 1"].str.contains('|'.join(legal_entities), case=False, na=False)]

# Извлечение уникальных имен физических лиц
names_list = pre_individuals_df["Owner Name 1"]

openai.api_key = config["API_KEY"]

names_string = "\n".join(names_list)

# Подготовка запроса к API
prompt = f"From the list below, identify which names are not names of people:\n{names_string}\n\n" \
         "Provide a only list of names that do not belong to people, without any other words."

# Отправка запроса к API
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",  
    messages=[
        {"role": "user", "content": prompt}
    ]
)

non_human_names = response.choices[0].message.content.split()

individuals_df = df[~df["Owner Name 1"].str.contains('|'.join(non_human_names), case=False, na=False)]

names_list = individuals_df["Owner Name 1"]

# Подсчет количества вхождений каждого имени
name_counts = Counter(names_list)

# Выбор имен, которые встречаются более одного раза
repeated_names = [name for name, count in name_counts.items() if count > 1]

# Запись в CSV-файл
with open("data/repeated_names.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Repeated Names"])  # Заголовок столбца
    for name in repeated_names:
        writer.writerow([name])  # Запись каждого имени в новую строку

print("Повторяющиеся имена записаны в файл repeated_names.csv.")