from selenium.webdriver.common.by import By
import time
import pandas as pd
from template import SeleniumAutomation  # Importa o template

class QuotesScraper(SeleniumAutomation):
    def __init__(self, headless=True):
        """Inicializa o scraper, herdando do template SeleniumAutomation"""
        super().__init__(headless=headless)

    def scrape_quotes(self):
        """Extrai todas as frases, autores e tags do site"""
        self.open_url("http://quotes.toscrape.com")

        quotes_data = []

        while True:
            quotes = self.get_elements_text("//span[@class='text']")
            authors = self.get_elements_text("//small[@class='author']")
            tags_lists = self.driver.find_elements(By.XPATH, "//div[@class='tags']/a[@class='tag']")

            for i in range(len(quotes)):
                tags = [tag.text for tag in tags_lists[i::len(quotes)]]  # Agrupa tags corretamente
                quotes_data.append({
                    "quote": quotes[i],
                    "author": authors[i],
                    "tags": ", ".join(tags)
                })

            # Verifica se há próxima página
            next_button = self.check_element_visible("//li[@class='next']/a")
            if next_button:
                self.click("//li[@class='next']/a")
                time.sleep(2)  # Espera pequena para carregamento
            else:
                break  # Sai do loop se não houver próxima página

        return quotes_data

    def save_to_csv(self, data, filename="quotes.csv"):
        """Salva os dados extraídos em um arquivo CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"Dados salvos em {filename}")

if __name__ == "__main__":
    scraper = QuotesScraper(headless=True)
    data = scraper.scrape_quotes()
    scraper.save_to_csv(data)
    scraper.close_browser()
