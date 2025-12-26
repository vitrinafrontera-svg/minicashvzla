import requests
from bs4 import BeautifulSoup
import datetime
import urllib3
import os

# Desactivar advertencias de seguridad para la web del BCV
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURACIÓN (GitHub leerá esto de tus 'Secrets') ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
BCV_URL = 'https://www.bcv.org.ve/'

def obtener_tasas():
    try:
        # Cabecera para que el BCV crea que somos un navegador normal
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(BCV_URL, headers=headers, verify=False, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer las tasas buscando por los IDs oficiales del BCV
            tasa_dolar = soup.find('div', id='dolar').find('strong').text.strip()
            tasa_euro = soup.find('div', id='euro').find('strong').text.strip()
            
            return tasa_dolar, tasa_euro
        else:
            print(f"Error BCV: Código de estado {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"Error haciendo scraping: {e}")
        return None, None

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    # Esto imprimirá en la consola de GitHub si Telegram aceptó el mensaje
    print(f"Respuesta de Telegram: {response.text}")

# --- EJECUCIÓN ---
dolar, euro = obtener_tasas()

if dolar and euro:
    fecha = datetime.datetime.now().strftime("%d/%m/%Y")
    
    mensaje = (
        f"📢 **Tasa Oficial BCV**\n"
        f"📅 **Fecha:** {fecha}\n\n"
        f"🇺🇸 **Dólar:** {dolar} Bs.\n"
        f"🇪🇺 **Euro:** {euro} Bs.\n\n"
        f"🔗 _Fuente: Banco Central de Venezuela_"
    )
    
    enviar_telegram(mensaje)
else:
    print("No se pudo obtener la información del BCV.")
