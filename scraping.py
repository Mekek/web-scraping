from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import csv
import json


# Загрузка конфигурации из JSON-файла
with open("config.json") as config_file:
    config = json.load(config_file)

# Настройка опций для безголового режима (если нужно)
options = Options()
options.add_argument("--headless")  # Запуск в фоновом режиме
service = Service(executable_path=config["CHROMEDRIVER_PATH"])  # Укажите путь к chromedriver

# Инициализация драйвера
driver = webdriver.Chrome(service=service, options=options)

rows = []

for offset in range(0, 650, 50):
    # URL сайта
    url = f"https://franklin.oh.publicsearch.us/results?_docTypes=MO&department=RP&limit=50&offset={offset}&recordedDateRange=20241014%2C20241018&searchOcrText=false&searchType=quickSearch"
    driver.get(url)

    # Ждем некоторое время, чтобы страница загрузилась
    time.sleep(5)  # Возможно, потребуется больше времени для загрузки

    # Получаем HTML-код страницы
    html = driver.page_source

    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Находим div с классом 'a11y-table'
    table_div = soup.find("div", class_="a11y-table")

    # Проверяем, найден ли div
    if table_div:
        # Находим таблицу
        table = table_div.find("table")

        # Извлекаем заголовки из thead
        headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]

        # Извлекаем записи из tbody
        for tr in table.find("tbody").find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all("td")]
            rows.append(cells)

        print(len(rows), "завершено на", len(rows) / 650 * 100, "%")
    else:
        print("Таблица не найдена на странице:", url)

# Закрываем драйвер
driver.quit()

# Запись в CSV-файл
with open("data/collected_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Запись заголовков
    writer.writerows(rows)    # Запись всех записей

print("Данные успешно записаны в файл collected_data.csv")


