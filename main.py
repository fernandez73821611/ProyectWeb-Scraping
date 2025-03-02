import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Ajusta la ruta a tu chromedriver
RUTA_CHROMEDRIVER = r"C:\driver\chromedriver.exe"

# Configurar Selenium
service = Service(RUTA_CHROMEDRIVER)
driver = webdriver.Chrome(service=service)

#creando listas para le dataframe
id_libros=[]
nombre_libros=[]
editorial_libros=[]
autor_libros=[]
anio_edicion=[]
paginas_libros=[]

try:
    #Abrir la página principal
    driver.get("https://www.sbs.com.pe/")
    time.sleep(5)  # Espera inicial para que cargue parte del contenido

    #Localizar el enlace "HABITOS ATOMICOS" y hacer clic
    wait = WebDriverWait(driver, 30)
    link_libro = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "HABITOS ATOMICOS"))
    )
    link_libro.click()

    #Esperar a que la URL contenga "habitos-atomicos.html"
    wait.until(EC.url_contains("habitos-atomicos.html"))
    time.sleep(3)  # Espera adicional para que la página de detalle cargue completamente

    #Obtener el HTML de la página de detalle y parsearlo
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    #Obetener el nombre del libro
    span_title = soup.find("span", class_="base", attrs={"data-ui-id": "page-title-wrapper", "itemprop": "name"})
    nombre_boock = span_title.get_text(strip=True) if span_title else "Nombre no encontrado"
    

    #Obtener el ID del libro
    etiqueta_id= soup.find("div", itemprop="sku")
    id_boock = etiqueta_id.get_text(strip=True) if etiqueta_id else "SKU no encontrado"

    #Obtener el precio
    etiqueta_precio= soup.find("span", class_="price")
    precio_boock = etiqueta_precio.get_text(strip=True) if etiqueta_precio else "Precio no encontrado"

    #obtener el editorial editorial 
    etiqueta_editorial = soup.find("th", text="Editorial")
    if etiqueta_editorial:
        etiqueta_editorial = etiqueta_editorial.find_next("td")
        editorial_boock= etiqueta_editorial.get_text(strip=True) if etiqueta_editorial else "Editorial no encontrada"
    else:
        editorial_boock = "Editorial no encontrada"

    # Obtener el nombre del libro
    etiqueta_autor= soup.find("th", text="Autor(es)")
    if etiqueta_autor:
        etiqueta_autor = etiqueta_autor.find_next("td")
        autor_boock= etiqueta_autor.get_text(strip=True) if etiqueta_autor else "Autor no encontrado"
    else:
        autor = "Autor no encontrado"

    # Obtener  el año de edición 
    etiqueta_año = soup.find("td", attrs={"data-th": "Año de edición"})
    anio_boock = etiqueta_año.get_text(strip=True) if etiqueta_año else "Año de edición no encontrado"

    # Obteniendo número de páginas
    etiqueta_paginas = soup.find("th", text="Páginas")
    if etiqueta_paginas:
        etiqueta_paginas = etiqueta_paginas.find_next("td")
        paginas_boock = etiqueta_paginas.get_text(strip=True) if etiqueta_paginas else "Número de páginas no encontrado"
    else:
        paginas_boock= "Número de páginas no encontrado"

    #agregando a las listas
    id_libros.append(id_boock)
    nombre_libros.append(nombre_boock)
    editorial_libros.append(editorial_boock)
    autor_libros.append(autor_boock)
    anio_edicion.append(anio_boock)
    paginas_libros.append(paginas_boock)

except Exception as e:
    print("Ocurrió un error:", e)
finally:
    driver.quit()


#creando un dataframe

df_libreria=pd.DataFrame(
    {
        "ID": id_libros,
        "NOMBRE":nombre_libros,
        "EDITORIAL":editorial_libros,
        "AUTOR":autor_libros,
        "ANIO": anio_edicion,
        "NUMERO PAGINAS":paginas_libros,
        
    }
)
df_libreria.to_csv("LibreriaInternacional.csv",index=False)
print("Datos Guardados Correctamente")