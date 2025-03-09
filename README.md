# UFORM

UFORM es una herramienta de automatización de formularios web desarrollada en Python, diseñada con fines educativos.

## Características

- **Automatización de formularios web:** Automatiza el llenado y envío de formularios mediante Selenium.
- **Menú interactivo:** Configura parámetros como URL, cantidad de envíos, campos de texto, checkboxes, radio buttons, comboBox y el botón de envío.
- **Multinavegador:** Soporta Chrome, Firefox (asegúrate de tener instalados los respectivos WebDrivers).
- **Manejo robusto de clics:** Utiliza métodos alternativos (JavaScript y ActionChains) para superar problemas con elementos tapados.

## Requisitos

- **Python:** 3.6 o superior.
- **Instalación**

   Crear el entorno virtual
    - python -m venv venv
   Activar el entorno virtual
    - Windows:   .\venv\Scripts\activate
    - Linux/Mac: source venv/bin/activate
   Instalar dependencias en el entorno virtual
    - pip install selenium pyfiglet
    - Ejecuta el script: python UForm.py

- **WebDrivers:** 
  - [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) para Google Chrome.
  - [GeckoDriver](https://github.com/mozilla/geckodriver/releases) para Firefox.
  - Drivers correspondientes para Edge y Safari.
  
*NOTA: segúrate de que el WebDriver que corresponda a tu navegador se encuentre en tu PATH o en el directorio del proyecto.*


