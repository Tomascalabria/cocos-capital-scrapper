from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
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
        self._url_movements='https://app.cocos.capital/movements/history'
        self.contraseña = contraseña
    
    def start(self):
        self.driver._driver.get(self._url_main)
        self.driver._driver.fullscreen_window()

        # Find the banner element using CSS selector
        user_input = self.driver._driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/div/input').send_keys(self.usuario)
        password_input = self.driver._driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div/input').send_keys(self.contraseña)
        btn = self.driver._driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[3]/button').click()
        time.sleep(5)
    
    def obtenerBalance(self):
        self.start()
        self.driver._driver.get(self._url_wallet)
        time.sleep(10)
        wait(self.driver._driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.heading-porftolio')))
        
        # Proceed with retrieving the element or performing actions on it
        element = self.driver._driver.find_element(By.CSS_SELECTOR, '.heading-porftolio')
        
        portfolio_heading = self.driver._driver.find_element(By.CLASS_NAME, 'heading-porftolio')
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
        new_date=input('Elija la desde que dia quiere obtener si no ingresa nada obtendrá todos.\n FORMATO: DD/MM/YYYY ')
        if new_date==' 'or new_date=='' or new_date=='  ':
             new_date='01/01/1990'
             print('Le mostraremos todos sus movimientos')
        else: 
             new_date
             print(f'Le mostraremos sus movimientos desde: {new_date}')
        time.sleep(10)
        self.start()
        self.driver._driver.get(self._url_movements)
        time.sleep(10)
        btn=self.driver._driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div/main/div[2]/div[1]/div/div/div[1]').click()
        date_input = self.driver._driver.find_element(By.ID, "outlined-adornment-weight")
        # Clear the current value (if any)
        date_input.clear()

        # Enter a new date value
        date_input.send_keys(new_date)
        time.sleep(5)

        