import requests
from bs4 import BeautifulSoup
from config import TIMEOUT

session = requests.Session()

def obtener_datos_libro(orden_id):
    try:
        url = "https://books.toscrape.com/catalogue/page-1.html"
        response = session.get(url, timeout=TIMEOUT)

        soup = BeautifulSoup(response.text, "html.parser")
        libros = soup.select("article.product_pod")

        if not libros:
            return None, None, None

        posicion = orden_id % 20
        libro = libros[posicion]

        titulo = libro.h3.a["title"]
        precio = libro.select_one(".price_color").text
        disponibilidad = libro.select_one(".availability").text.strip()

        return titulo, precio, disponibilidad

    except Exception:
        return None, None, None