import json
import os


class GestorJSON:
    """Lee y escribe listas de diccionarios en archivos JSON."""

    def __init__(self, ruta):
        self.ruta = ruta
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)
        if not os.path.exists(ruta):
            self.guardar([])

    def leer(self):
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                return contenido if isinstance(contenido, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
