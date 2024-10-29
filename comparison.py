import pandas as pd

# Загрузка данных из CSV-файлов
collected_data = pd.read_csv("data/collected_data.csv")
average_inventory = pd.read_csv("data/average_inventory.csv")

# Получаем номера Parcel Number из average_inventory
parcel_numbers = average_inventory['Parcel Number'].astype(str).tolist()

# Фильтрация collected_data, оставляя только записи, в которых Legal Description содержит Parcel Number
filtered_data = collected_data[collected_data['Legal Description'].str.contains('|'.join(parcel_numbers), na=False)]

# Преобразование Legal Description для выделения Parcel Number
filtered_data['Parcel Number'] = filtered_data['Legal Description'].str.extract(r'(\d{3}-\d{6}-\d{2})')[0]

# Объединение таблиц по Parcel Number с использованием left join, чтобы сохранить строки из filtered_data
final_data = pd.merge(filtered_data, average_inventory, on='Parcel Number', how='left')

# Сохранение результата в новый CSV-файл
final_data.to_csv("data/compared_data.csv", index=False)

print("Финальная таблица сохранена в data/compared_data.csv")
