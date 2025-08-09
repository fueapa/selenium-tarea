from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# Ruta al ejecutable de Brave (cambia por la ruta correcta en tu PC)
brave_path = r"C:\Users\El apa\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"

# Ruta al chromedriver.exe (asegúrate que está en esa ruta)
driver_path = r"C:\Users\El apa\Desktop\selenium-drivers\chromedriver.exe"

options = webdriver.ChromeOptions()
options.binary_location = brave_path

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.google.com")
time.sleep(5)
driver.quit()
