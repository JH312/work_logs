import re
import json
import requests

# URL del archivo de log
url = 'https://raw.githubusercontent.com/elastic/examples/refs/heads/master/Common%20Data%20Formats/apache_logs/apache_logs'
datos = []

# Patrones o parametros ajustados a lo que se pide en la actividad
fecha_patron = r'\[(\d{2}/[A-Za-z]+/\d{4}:\d{2}:\d{2}:\d{2})'
ip_patron = r'^(\d+\.\d+\.\d+\.\d+)'
metodo_patron = r'"(GET|POST|PUT|DELETE|HEAD|OPTIONS)'
recurso_patron = r'"[A-Z]+ (\/[^\s]*)'
estado_patron = r'" (\d{3}) '
agente_patron = r'"([^"]*)"$'

# Descargar el archivo desde la URL
response = requests.get(url)
if response.status_code == 200:
    # Procesar cada línea del contenido alojado en el link
    for linea in response.text.splitlines():
        fecha = re.search(fecha_patron, linea)
        ip = re.search(ip_patron, linea)
        metodo = re.search(metodo_patron, linea)
        recurso = re.search(recurso_patron, linea)
        estado = re.search(estado_patron, linea)
        agente = re.search(agente_patron, linea)

        log_entrada = {
            "fecha": fecha.group(1) if fecha else None,
            "ip": ip.group(1) if ip else None,
            "metodo": metodo.group(1) if metodo else None,
            "recurso": recurso.group(1) if recurso else None,
            "estado": estado.group(1) if estado else None,
            "agente": agente.group(1) if agente else None
        }
        datos.append(log_entrada)

    # Guarda los datos en un archivo JSON
    with open('log_datos.json', 'w') as json_file:
        json.dump(datos, json_file, indent=4)

    print("Datos extraídos y guardados en 'log_datos.json'.")

else:
    print(f"Error al acceder a la URL: {response.status_code}")
