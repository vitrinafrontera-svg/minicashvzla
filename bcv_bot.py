import requests
from bs4 import BeautifulSoup
import os
import urllib3

# Desactiva avisos de seguridad por el certificado del BCV
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def obtener_datos_bcv():
    url = 'https://www.bcv.org.ve/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extraer tasas
            dolar = soup.find('div', id='dolar').find('strong').text.strip()
            euro = soup.find('div', id='euro').find('strong').text.strip()
            return dolar, euro
    except Exception as e:
        print(f"Error al obtener datos: {e}")
    return None, None

def enviar_a_telegram(dolar, euro):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    
    if not token or not chat_id:
        print("Error: No se encontraron las variables TELEGRAM_TOKEN o CHAT_ID")
        return

    mensaje = (
        f"📊 **Tasa Oficial BCV**\n\n"
        f"💵 **Dólar:** {dolar} Bs.\n"
        f"💶 **Euro:** {euro} Bs.\n\n"
        f"🏛 _Fuente: Banco Central de Venezuela_"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
    
    r = requests.post(url, data=payload)
    print(f"Resultado Telegram: {r.text}")

if __name__ == "__main__":
    tasa_dolar, tasa_euro = obtener_datos_bcv()
    if tasa_dolar:
        enviar_a_telegram(tasa_dolar, tasa_euro)
    else:
        print("No se pudo procesar la información.")
