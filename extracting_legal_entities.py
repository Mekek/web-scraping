import pandas as pd

# Загрузка данных из CSV-файла
data = pd.read_csv("data/compared_data.csv")

# Фильтрация строк, где "Owner Name 1" содержит LLC, LTD, INC или TR, без учета регистра
filtered_data = data[
    data['Owner Name 1'].str.contains(r'\b(LLC|LTD|INC|TR)\b', case=False, na=False)
]

# Сохранение результата в новый CSV-файл
filtered_data.to_csv("data/legal_entities.csv", index=False)

print("Фильтрованные данные сохранены в data/legal_entities.csv")
