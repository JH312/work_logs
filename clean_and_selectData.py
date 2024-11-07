import re
import json
import requests
from collections import Counter

# URL del archivo de log
url = 'https://raw.githubusercontent.com/elastic/examples/refs/heads/master/Common%20Data%20Formats/apache_logs/apache_logs'
datos = []

# Patrones ajustados
fecha_patron = r'\[(\d{2}/[A-Za-z]+/\d{4}:\d{2}:\d{2}:\d{2})'
ip_patron = r'^(\d+\.\d+\.\d+\.\d+)'
metodo_patron = r'"(GET|POST|PUT|DELETE|HEAD|OPTIONS)'
recurso_patron = r'"[A-Z]+ (\/[^\s]*)'
estado_patron = r'" (\d{3}) '
agente_patron = r'"([^"]*)"$'

# Contadores adicionales
ip_counter = Counter()      # Contador de solicitudes por IP
estado_4xx_5xx = []         # Lista para almacenar líneas con códigos de estado 4xx y 5xx
recurso_counter = Counter()  # Contador de solicitudes por recurso

# Descargar el archivo desde la URL
response = requests.get(url)
if response.status_code == 200:
    # Procesar cada línea del contenido
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

        # Incrementar el contador de solicitudes por IP
        if ip:
            ip_counter[ip.group(1)] += 1

        # Almacenar las líneas con códigos de estado 4xx y 5xx
        if estado and estado.group(1).startswith(('4', '5')):
            estado_4xx_5xx.append(log_entrada)

        # Incrementar el contador de solicitudes por recurso
        if recurso:
            recurso_counter[recurso.group(1)] += 1

    # Guarda los datos en un archivo JSON
    with open('log_datos.json', 'w') as json_file:
        json.dump(datos, json_file, indent=4)

    # Guarda el conteo de solicitudes por IP
    with open('conteo_ip.json', 'w') as json_file:
        json.dump(ip_counter, json_file, indent=4)

    # Guarda las líneas con códigos de estado 4xx y 5xx
    with open('errores_4xx_5xx.json', 'w') as json_file:
        json.dump(estado_4xx_5xx, json_file, indent=4)

    # Guarda el conteo de solicitudes por recurso
    with open('conteo_recursos.json', 'w') as json_file:
        json.dump(recurso_counter, json_file, indent=4)

    print("Datos extraídos y guardados en los archivos JSON correspondientes.")

else:
    print(f"Error al acceder a la URL: {response.status_code}")
