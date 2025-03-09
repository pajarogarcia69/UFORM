import time
import logging
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyfiglet

# Función para limpiar la consola 
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def safe_int_input(prompt, default=None):
    while True:
        user_input = input(prompt).strip()
        if user_input == "" and default is not None:
            return default
        try:
            return int(user_input)
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número entero.")


def safe_str_input(prompt, default=None):
    while True:
        user_input = input(prompt).strip()
        if user_input == "" and default is not None:
            return default
        elif user_input != "":
            return user_input
        else:
            print("La entrada no puede estar vacía.")

def init_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

logger = init_logger()

def robust_click(element, driver):
    try:
        element.click()
    except Exception as e:
        logger.error("Error en click normal: %s. Se intenta click con JavaScript.", e)
        try:
            driver.execute_script("arguments[0].click();", element)
        except Exception as e2:
            logger.error("Error en click con JavaScript: %s. Se intenta click con ActionChains.", e2)
            try:
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
            except Exception as e3:
                logger.error("Error en click con ActionChains: %s", e3)

def get_browser_choice():
    print("**** Seleccione el tipo de navegador ****")
    print("1. Google Chrome")
    print("2. Firefox")
    choice = safe_str_input("Ingrese el número del navegador (default 1): ", default="1")
    browser_map = {'1': 'chrome', '2': 'firefox' }
    return browser_map.get(choice, 'chrome')

def init_webdriver(browser_choice):
    try:
        if browser_choice == 'chrome':
            driver = webdriver.Chrome()
        elif browser_choice == 'firefox':
            driver = webdriver.Firefox()
        else:
            logger.error("Opción de navegador no válida.")
            sys.exit(1)
        return driver
    except Exception as e:
        logger.error("Error al iniciar el navegador: %s", e)
        sys.exit(1)

def display_menu():
    clear_console()

    print(pyfiglet.figlet_format("UFORM"))
    print("\n===== MENÚ UFORM =====")
    print("1. Modificar URL del formulario")
    print("2. Modificar cantidad de repeticiones (envíos)")
    print("3. Modificar cantidad de campos de texto y sus valores")
    print("4. Modificar cantidad de checkbox y sus XPATH")
    print("5. Modificar cantidad de radio buttons y sus XPATH")
    print("6. Modificar cantidad de comboBox y sus opciones")
    print("7. Modificar XPATH del botón de envío")
    print("8. Modificar navegador a utilizar")
    print("9. Ver parámetros actuales")
    print("10. Iniciar automatización")
    print("0. Salir")
    print("=======================")

def review_params(params):
    clear_console()
    print(pyfiglet.figlet_format("UFORM"))
    print("\n===== PARÁMETROS ACTUALES =====")
    print(f"URL: {params['url']}")
    print(f"Repeticiones: {params['repeticiones']}")
    print(f"Cantidad de campos de texto: {params['campos']}")
    print(f"Cantidad de checkbox: {params['checkbox']}")
    print(f"Cantidad de radio buttons: {params['radio']}")
    print(f"Cantidad de comboBox: {params['select']}")
    print(f"XPATH del botón de envío: {params['send_button_xpath']}")
    print(f"Navegador: {params['browser']}")
    if params['campos'] > 0:
        print("Campos de texto:")
        for i, (xpath, value) in enumerate(zip(params['text_xpaths'], params['text_values']), start=1):
            print(f"   {i}. XPATH: {xpath}  Valor: {value}")
    if params['checkbox'] > 0:
        print("Checkbox:")
        for i, xpath in enumerate(params['checkbox_xpaths'], start=1):
            print(f"   {i}. XPATH: {xpath}")
    if params['radio'] > 0:
        print("Radio buttons:")
        for i, xpath in enumerate(params['radio_xpaths'], start=1):
            print(f"   {i}. XPATH: {xpath}")
    if params['select'] > 0:
        print("ComboBox y Opciones:")
        for i, (combo, option) in enumerate(zip(params['select_xpaths'], params['option_xpaths']), start=1):
            print(f"   {i}. ComboBox: {combo}  Opción: {option}")
    print("=======================")
    input("Presione Enter para continuar...")

def modify_params(params):
    while True:
        display_menu()
        choice = safe_str_input("Seleccione una opción del menú: ")
        if choice == '1':
            params['url'] = safe_str_input("Ingrese la URL del formulario: ")
        elif choice == '2':
            params['repeticiones'] = safe_int_input("Ingrese la cantidad de repeticiones (envíos): ")
        elif choice == '3':
            params['campos'] = safe_int_input("Ingrese la cantidad de campos de texto: ")
            params['text_xpaths'] = []
            params['text_values'] = []
            for i in range(params['campos']):
                xpath = safe_str_input(f"Ingrese el XPATH del campo de texto {i+1}: ")
                value = safe_str_input(f"Ingrese el valor para el campo {i+1}: ")
                params['text_xpaths'].append(xpath)
                params['text_values'].append(value)
        elif choice == '4':
            params['checkbox'] = safe_int_input("Ingrese la cantidad de checkbox (0 si no hay): ")
            params['checkbox_xpaths'] = []
            for i in range(params['checkbox']):
                xpath = safe_str_input(f"Ingrese el XPATH del checkbox {i+1}: ")
                params['checkbox_xpaths'].append(xpath)
        elif choice == '5':
            params['radio'] = safe_int_input("Ingrese la cantidad de radio buttons (0 si no hay): ")
            params['radio_xpaths'] = []
            for i in range(params['radio']):
                xpath = safe_str_input(f"Ingrese el XPATH del radio button {i+1}: ")
                params['radio_xpaths'].append(xpath)
        elif choice == '6':
            params['select'] = safe_int_input("Ingrese la cantidad de comboBox (0 si no hay): ")
            params['select_xpaths'] = []
            params['option_xpaths'] = []
            for i in range(params['select']):
                combo = safe_str_input(f"Ingrese el XPATH del comboBox {i+1}: ")
                option = safe_str_input(f"Ingrese el XPATH de la opción a seleccionar {i+1}: ")
                params['select_xpaths'].append(combo)
                params['option_xpaths'].append(option)
        elif choice == '7':
            params['send_button_xpath'] = safe_str_input("Ingrese el XPATH del botón de envío: ")
        elif choice == '8':
            params['browser'] = get_browser_choice()
        elif choice == '9':
            review_params(params)
        elif choice == '10':
            review_params(params)
            confirm = safe_str_input("¿Está todo correcto? (s/n): ").lower()
            if confirm == 's':
                return params
        elif choice == '0':
            logger.info("Saliendo de UForm.")
            sys.exit(0)
        else:
            print("Opción no válida. Intente nuevamente.")
        time.sleep(1)

def execute_automation(params):
    navegador = init_webdriver(params['browser'])
    navegador.get(params['url'])
    navegador.maximize_window()
    wait = WebDriverWait(navegador, 20)
    
    try:
        if params['checkbox'] > 0:
            for xpath in params['checkbox_xpaths']:
                try:
                    check = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    navegador.execute_script("arguments[0].scrollIntoView(true);", check)
                    robust_click(check, navegador)
                    time.sleep(1)
                except Exception as e:
                    logger.error("Error en checkbox (%s): %s", xpath, e)
        if params['radio'] > 0:
            for xpath in params['radio_xpaths']:
                try:
                    radio = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    navegador.execute_script("arguments[0].scrollIntoView(true);", radio)
                    robust_click(radio, navegador)
                    time.sleep(1)
                except Exception as e:
                    logger.error("Error en radio button (%s): %s", xpath, e)
        if params['select'] > 0:
            for combo_xpath, option_xpath in zip(params['select_xpaths'], params['option_xpaths']):
                try:
                    combo = wait.until(EC.presence_of_element_located((By.XPATH, combo_xpath)))
                    navegador.execute_script("arguments[0].scrollIntoView(true);", combo)
                    time.sleep(1)  
                    robust_click(combo, navegador)
                    time.sleep(5)  
                    option = wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
                    navegador.execute_script("arguments[0].scrollIntoView(true);", option)
                    time.sleep(1)
                    robust_click(option, navegador)
                    time.sleep(1)
                except Exception as e:
                    logger.error("Error en comboBox (%s): %s", combo_xpath, e)
     
        if params['campos'] > 0:
            for xpath, value in zip(params['text_xpaths'], params['text_values']):
                try:
                    textbox = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    navegador.execute_script("arguments[0].scrollIntoView(true);", textbox)
                    textbox.clear()
                    textbox.send_keys(value)
                    time.sleep(1)
                except Exception as e:
                    logger.error("Error en campo de texto (%s): %s", xpath, e)
      
        if params['send_button_xpath']:
            for j in range(params['repeticiones']):
                try:
                    boton = wait.until(EC.element_to_be_clickable((By.XPATH, params['send_button_xpath'])))
                    navegador.execute_script("arguments[0].scrollIntoView(true);", boton)
                    robust_click(boton, navegador)
                    logger.info("Formulario enviado %d/%d", j+1, params['repeticiones'])
                    time.sleep(5)
                except Exception as e:
                    logger.error("Error al enviar formulario en iteración %d: %s", j+1, e)
        else:
            logger.error("No se ha especificado el XPATH del botón de envío.")
    except Exception as e:
        logger.error("Error durante la automatización: %s", e)
    finally:
        logger.info("Cerrando el navegador...")
        navegador.quit()

def main():
   
    params = {
        'url': '',
        'repeticiones': 1,
        'campos': 1,
        'checkbox': 1,
        'radio': 0,
        'select': 1,
        'send_button_xpath': '',
        'text_xpaths': [
        ],
        'text_values': [
            "",
            "",
            "",
            "",
            ""
        ],
        'checkbox_xpaths': [
            ""
        ],
        'radio_xpaths': [],
        'select_xpaths': [
            ""
        ],
        'option_xpaths': [
            ""
        ],
        'browser': ''
    }
    
    while True:
        clear_console()
        print(pyfiglet.figlet_format("UFORM"))
        logger.info("Bienvenido a UFORM, herramienta de automatización de formularios (uso educativo)")
        # Permitir al usuario modificar y revisar parámetros con el menú dinámico
        params = modify_params(params)
        review_params(params)
        confirm = safe_str_input("¿Desea iniciar la automatización? (s/n): ").lower()
        if confirm == 's':
            execute_automation(params)
            safe_str_input("Automatización completada. Presione Enter para volver al menú...")
        else:
            logger.info("Automatización cancelada.")
            safe_str_input("Presione Enter para volver al menú...")

if __name__ == "__main__":
    main()


"""
================================================================================
Autor: Steven Pajaro Garcia
Proyecto: UFORM - Automatización de Formularios Web
Descripción: Esta herramienta permite automatizar el llenado y envío de
formularios web utilizando Selenium.
================================================================================
"""