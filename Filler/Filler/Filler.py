# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os

CSV_FILE = "productos.csv"           
SENT_FILE = "enviados.txt"              
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeKaqoCckpBcN4oohQ3VV3_DhPbCYjotk0byBkMB6WmpEURqg/viewform"

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # Solo errores fatales
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Oculta logs de Chrome
driver = webdriver.Chrome(service=service, options=options)

def cargar_enviados():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def guardar_enviado(identificador):
    with open(SENT_FILE, "a", encoding="utf-8") as f:
        f.write(identificador + "\n")

def completar_formulario(dni, dia, producto):
    driver.get(FORM_URL)

    # tiempo de espera
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']")))
    
    campos = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    campos[0].send_keys(dni)
    campos[1].send_keys(dia)
    campos[2].send_keys(producto)

    # seleccionar boton de envio
    boton = driver.find_element(By.XPATH, "//span[contains(text(),'Enviar') or contains(text(),'Submit')]")
    boton.click()

    # espera 1 segundo para recargar la pagina
    time.sleep(1)

#guardar datos enviados
enviados = cargar_enviados()

with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        id_unico = f"{row['DNI']}_{row['DIA']}"
        if id_unico in enviados:
            continue

        print("NO CERRAR VENTANA DE CHROME MIENTRAS EL PROGRAMA ESTA FUNCIONANDO")
        print(f"Enviando: Dni {row['DNI']} del dia {row['DIA']} con el producto {row['PRODUCTO']}")
        completar_formulario(row['DNI'], row['DIA'], row['PRODUCTO'])
        guardar_enviado(id_unico)
        input("Presiona ENTER para enviar el siguiente producto...")


driver.quit()
