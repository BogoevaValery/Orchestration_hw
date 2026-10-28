from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")  # Тот самый headless режим. Можно использовать "--headless=new"
options.add_argument("--disable-gpu")  # Отключаем GPU для стабильности
options.add_argument("--no-sandbox")  # Нужно для Linux
options.add_argument("--window-size=1920,1080")  # Размер окна

driver = webdriver.Firefox(options=options)  # Если нужно - указываем путь к браузеру

driver.get("https://example.com")
print(driver.title)  # Выведет заголовок страницы ("Example Domain")

from selenium.webdriver.common.by import By
element = driver.find_element(By.CSS_SELECTOR, "h1")
print(element.text)

# Найти элемент по ID
element = driver.find_element(By.ID, "main")
print(element.text)