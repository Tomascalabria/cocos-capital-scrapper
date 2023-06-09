from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

import time
from tabulate import tabulate
from Driver import Driver
from datetime import datetime


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
    def obtenerTodosMovimientos(self):
        new_date = '11041999'
        time.sleep(4)
        self.start()
        self.driver._driver.get(self._url_movements)
        time.sleep(4)
        btn = self.driver._driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/main/div[2]/div[1]/div/div/div[1]').click()
        date_input = self.driver._driver.find_element(By.ID, "outlined-adornment-weight")
    
        # Enter a new date value
        date_input.send_keys(new_date)
        time.sleep(1)
    
        # Click on the Apply Filters button
        apply_filters = self.driver._driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div/div[2]/div/div[2]/button')
        apply_filters.click()
        time.sleep(20)
    
        # Simulate keyboard event to close the filter or overlay element
        actions = ActionChains(self.driver._driver)
        time.sleep(13)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
    
        # Extract the movements data using Selenium
        movements = self.driver._driver.find_elements(By.XPATH, "//div[@class='grid-desktop']")
    
        time.sleep(5)
        buy_sell_data = []
        deposit_extraction_data = []
        
        for row in movements:
            cells = row.find_elements(By.TAG_NAME, 'span')
            operation_parts = cells[0].text.split()
            ticker = operation_parts[0]
            if len(operation_parts) > 1:
                operation = operation_parts[1]
                type = cells[1].text
                day = cells[2].text
                quantity = cells[3].text if cells[3].text else ""
                total_movement = cells[4].text
                status = cells[5].text
                buy_sell_data.append([ticker, operation, type, day, quantity, total_movement, status])
            else:
                operation = cells[1].text
                type = ""  # Add an empty string for type in deposits/extractions
                day = cells[2].text
                quantity = cells[3].text if cells[3].text else ""
                total_movement = cells[4].text
                status = cells[5].text
                deposit_extraction_data.append([ticker, operation, type, day, quantity, total_movement, status])
        
        buy_sell_headers = ['Ticker', 'Operación', 'Tipo', 'Día', 'Cantidad', 'Total Movimiento', 'Estado']
        deposit_extraction_headers = ['', 'Operación', 'Tipo', 'Día', 'Cantidad', 'Total Movimiento', 'Estado']  # Add an empty string as the first header
        
        buy_sell_table = tabulate(buy_sell_data, buy_sell_headers, tablefmt='grid')
        deposit_extraction_table = tabulate(deposit_extraction_data, deposit_extraction_headers, tablefmt='grid')
        
        print('\033[1m--------------- MOVIMIENTOS DE COMPRA Y VENTA: COCOS CAPITAL -----------------\033[0m \n')
        print(buy_sell_table)
        
        print('\n')
        
        print('\033[1m--------------- MOVIMIENTOS DE DEPÓSITO Y EXTRACCIÓN: COCOS CAPITAL -----------------\033[0m \n')
        print(deposit_extraction_table)
        