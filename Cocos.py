from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tabulate import tabulate
from Driver import Driver

class Cocos:
    def __init__(self, driver, usuario, contraseña):
        self.usuario = usuario
        self.driver = driver
        self._url_main = 'https://app.cocos.capital/login'
        self._url_wallet = 'https://app.cocos.capital/wallet'
        self._url_movements = 'https://app.cocos.capital/movements/history'
        self.contraseña = contraseña

    def start(self):
        self.driver._driver.get(self._url_main)
        self.driver._driver.maximize_window()

        user_input = self.driver._driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/div/input')
        user_input.send_keys(self.usuario)

        password_input = self.driver._driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/input')
        password_input.send_keys(self.contraseña)

        btn = self.driver._driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[3]/button')
        btn.click()

        time.sleep(5)

    def obtenerBalance(self):
        self.start()
        self.driver._driver.get(self._url_wallet)
        wait = WebDriverWait(self.driver._driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'heading-portfolio')))

        portfolio_heading = self.driver._driver.find_element(By.CLASS_NAME, 'heading-portfolio')
        value_element = portfolio_heading.find_element(By.CLASS_NAME, 'MuiTypography-heading3_bold')
        balance = value_element.text

        holding_rows = self.driver._driver.find_elements(By.CLASS_NAME, 'comp-holding-row-desktop')

        data = []

        for row in holding_rows:
            ticker_element = row.find_element(By.CLASS_NAME, 'short_ticker')
            ticker = ticker_element.find_element(By.CLASS_NAME, 'MuiTypography-textS').text

            variation_element = row.find_element(By.CLASS_NAME, 'last')
            variation = variation_element.find_element(By.CLASS_NAME, 'MuiTypography-textS').text

            price_element = row.find_element(By.CSS_SELECTOR, '.grid-col:nth-child(4) > span')
            price = price_element.text

            quantity_element = row.find_element(By.CSS_SELECTOR, '.grid-col:nth-child(5) > span')
            quantity = quantity_element.text

            amount_element = row.find_element(By.CSS_SELECTOR, '.amount-container .MuiTypography-textS')
            amount = amount_element.text

            data.append([ticker, variation, f'${price}', quantity, f'${amount}'])

        headers = ['Ticker', 'Variation', 'Price', 'Quantity', 'Amount']
        table = tabulate(data, headers, tablefmt='grid')

        print('\033[1m--------------- ESTADO DE CUENTA: COCOS CAPITAL-----------------\033[0m \n')
        print(table)
        print(f'Balance en cuenta: ${balance}')

    def obtenerMovimientos(self):
        new_date = input('Elija la fecha desde la cual quiere obtener los movimientos (DD/MM/YYYY). Si no ingresa nada, se obtendrán todos los movimientos: ')
        if not new_date.strip():
            new_date = '01/01/1990'
            print('Le mostraremos todos sus movimientos')
        else:
            print(f'Le mostraremos sus movimientos desde: {new_date}')

        self.start()
        self.driver._driver.get(self._url_movements)
        time.sleep(10)

        btn = self.driver._driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/main/div[2]/div[1]/div/div/div[1]')
        btn.click()

        date_input = self.driver._driver.find_element(By.ID, "outlined-adornment-weight")
        date_input.clear()
        date_input.send_keys(new_date)

        time.sleep(5)
    # To be added ...