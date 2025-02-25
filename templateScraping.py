#Dependencias
#pip install selenium
#pip install webdriver-manager

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumAutomation:
    def __init__(self, headless=False, download_path=None):
        """Inicializa o driver do Chrome automaticamente e configura o diretório de downloads."""
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")  # Abre a janela maximizada
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-popup-blocking")

        if headless:
            self.options.add_argument("--headless")  # Executar sem interface gráfica
        
        # Configuração de diretório para downloads (se especificado)
        if download_path:
            prefs = {"download.default_directory": os.path.abspath(download_path)}
            self.options.add_experimental_option("prefs", prefs)

        # Instala e inicia o WebDriver automaticamente
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.wait = WebDriverWait(self.driver, 10)  # Espera máxima de 10 segundos

    def open_url(self, url):
        """Abre uma URL no navegador."""
        self.driver.get(url)
        print(f"Abrindo URL: {url}")

    def click(self, locator, locator_type=By.XPATH, apelido=None):
        """Clica em um elemento específico."""
        element = self.wait.until(EC.element_to_be_clickable((locator_type, locator)))
        element.click()
        print(f"Elemento clicado: {locator} apelidado de {apelido}")

    def double_click(self, locator, locator_type=By.XPATH):
        """Realiza um clique duplo em um elemento."""
        element = self.wait.until(EC.element_to_be_clickable((locator_type, locator)))
        action = ActionChains(self.driver)
        action.double_click(element).perform()
        print(f"Duplo clique no elemento: {locator}")

    def send_keys(self, locator, text, locator_type=By.XPATH, clear=True):
        """Envia texto para um campo de entrada."""
        element = self.wait.until(EC.presence_of_element_located((locator_type, locator)))
        if clear:
            element.clear()
        element.send_keys(text)
        print(f"Texto enviado: '{text}' para {locator}")

    def check_element_visible(self, locator, locator_type=By.XPATH):
        """Verifica se um elemento está visível na página."""
        try:
            self.wait.until(EC.visibility_of_element_located((locator_type, locator)))
            print(f"Elemento visível: {locator}")
            return True
        except:
            print(f"Elemento não encontrado ou não visível: {locator}")
            return False

    def scroll_to_element(self, locator, locator_type=By.XPATH):
        """Rola a página até um elemento específico."""
        element = self.wait.until(EC.presence_of_element_located((locator_type, locator)))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        print(f"Rolando até o elemento: {locator}")

    def switch_to_iframe(self, locator, locator_type=By.XPATH):
        """Entra em um iframe específico."""
        iframe = self.wait.until(EC.presence_of_element_located((locator_type, locator)))
        self.driver.switch_to.frame(iframe)
        print(f"Entrou no iframe: {locator}")

    def switch_to_default(self):
        """Sai do iframe e volta para o contexto principal."""
        self.driver.switch_to.default_content()
        print("Saiu do iframe e voltou para o contexto principal.")

    def get_text(self, locator, locator_type=By.XPATH):
        """Captura o texto de um elemento na página."""
        element = self.wait.until(EC.presence_of_element_located((locator_type, locator)))
        text = element.text
        print(f"Texto extraído: {text}")
        return text

    def get_elements_text(self, locator, locator_type=By.XPATH):
        """Captura o texto de múltiplos elementos na página."""
        elements = self.wait.until(EC.presence_of_all_elements_located((locator_type, locator)))
        texts = [element.text for element in elements]
        print(f"Textos extraídos: {texts}")
        return texts

    def get_attribute(self, locator, attribute, locator_type=By.XPATH):
        """Captura um atributo específico de um elemento."""
        element = self.wait.until(EC.presence_of_element_located((locator_type, locator)))
        attr_value = element.get_attribute(attribute)
        print(f"Atributo '{attribute}' extraído: {attr_value}")
        return attr_value

    def execute_script(self, script, *args):
        """Executa JavaScript na página."""
        result = self.driver.execute_script(script, *args)
        print(f"Script executado: {script}")
        return result

    def take_screenshot(self, filename="screenshot.png"):
        """Captura um screenshot da página."""
        self.driver.save_screenshot(filename)
        print(f"Screenshot salvo como: {filename}")

    def download_file(self, locator, locator_type=By.XPATH):
        """Clica em um botão de download e aguarda o download ser concluído."""
        self.click(locator, locator_type)
        time.sleep(5)  # Ajuste conforme o tempo médio de download do site
        print(f"Download iniciado via {locator}")

    def close_browser(self):
        """Fecha o navegador e encerra o WebDriver."""
        self.driver.quit()
        print("Navegador fechado.")

if __name__ == "__main__":
    bot = SeleniumAutomation(headless=False, download_path="downloads")  
    bot.open_url("https://example.com")
