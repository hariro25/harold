from flask import Flask, request, render_template_string
import requests
import csv
from datetime import datetime
import os

app = Flask(__name__)

html = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Conectando...</title>
    <style>
        body { 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            background-color: #f0f0f0; 
            font-family: Arial, sans-serif;
        }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Conectando con el servidor...</h1>
</body>
</html>
'''


def get_location_from_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return data
    except Exception as e:
        print(f"Error obteniendo localización: {e}")
        return {}


def save_visit(data):
    file_exists = os.path.isfile('visitas.csv')

    with open('visitas.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['Fecha', 'Hora', 'IP', 'Ciudad', 'Región', 'País', 'Localización', 'Organización'])

        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')

        writer.writerow([
            date, time,
            data.get('ip', 'N/A'),
            data.get('city', 'N/A'),
            data.get('region', 'N/A'),
            data.get('country', 'N/A'),
            data.get('loc', 'N/A'),
            data.get('org', 'N/A')
        ])


@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"IP capturada: {ip}")

    location = get_location_from_ip(ip)
    print(f"Datos de geolocalización: {location}")

    save_visit(location)

    return render_template_string(html)


if __name__ == '_main_':
    app.run(host="0.0.0.0", port=10000)
