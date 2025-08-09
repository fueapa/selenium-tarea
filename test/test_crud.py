from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import unittest
import os
import HtmlTestRunner  

class TestCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        brave_path = r"C:\Users\El apa\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"
        driver_path = r"C:\Users\El apa\Desktop\selenium-drivers\chromedriver.exe"

        options = webdriver.ChromeOptions()
        options.binary_location = brave_path
        service = Service(driver_path)
        cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver.maximize_window()

        # crea carpetas si no existen 
        cls.screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        cls.reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(cls.screenshots_dir, exist_ok=True)
        os.makedirs(cls.reports_dir, exist_ok=True)

    def tearDown(self):
        # captura de pantalla si falla la prueba (creo que funciona)
        failed = False
        result = getattr(self._outcome, 'result', None)
        if result:
            for test, exc_info in result.errors + result.failures:
                if test.id() == self.id():
                    failed = True
                    break

        if failed:
            timestamp = int(time.time())
            screenshot_path = os.path.join(self.screenshots_dir, f"{self._testMethodName}_{timestamp}.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"Captura tomada: {screenshot_path}")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_crear_usuario(self):
        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(1)

        crear_link = self.driver.find_element(By.LINK_TEXT, "Crear nuevo usuario")
        crear_link.click()
        time.sleep(1)

        self.driver.find_element(By.NAME, "nombre").send_keys("Manuel Rodriguez")
        self.driver.find_element(By.NAME, "email").send_keys("manuel@example.com")

        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        usuarios = self.driver.find_elements(By.TAG_NAME, "li")
        textos = [u.text for u in usuarios]
        self.assertTrue(any("Manuel Rodriguez" in texto for texto in textos))

    def test_editar_usuario(self):
        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(1)

        editar_link = self.driver.find_element(By.LINK_TEXT, "Editar")
        editar_link.click()
        time.sleep(1)

        nombre_input = self.driver.find_element(By.NAME, "nombre")
        nombre_input.clear()
        nombre_input.send_keys("Manuel Editado")

        email_input = self.driver.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys("manuel.editado@example.com")

        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        usuarios = self.driver.find_elements(By.TAG_NAME, "li")
        textos = [u.text for u in usuarios]
        self.assertTrue(any("Manuel Editado" in texto for texto in textos))

    def test_eliminar_usuario(self):
        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(1)

        eliminar_link = self.driver.find_element(By.LINK_TEXT, "Eliminar")
        eliminar_link.click()
        time.sleep(1)

        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(2)

        usuarios = self.driver.find_elements(By.TAG_NAME, "li")
        textos = [u.text for u in usuarios]
        self.assertFalse(any("Manuel Editado" in texto for texto in textos))


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'))
