import requests
from bs4 import BeautifulSoup
import datetime
import urllib3

# Desactivar advertencias de certificado SSL (común en sitios gubernamentales)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURACIÓN ---
TELEGRAM_TOKEN = '8349779265:AAF5Wx-8hCdk0jzm0uXQd8n2jXHrhZgGI1U'
CHAT_ID = '1003356621812' # Ej: -10012345678
BCV_URL = 'https://www.bcv.org.ve/'

def obtener_tasas():
    try:
        # El sitio del BCV a veces tiene problemas de certificados, por eso verify=False
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(BCV_URL, headers=headers, verify=False, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # NOTA: El BCV cambia su estructura a veces. 
            # Actualmente las tasas están en divs con id "dolar" y "euro"
            tasa_dolar = soup.find('div', id='dolar').find('strong').text.strip()
            tasa_euro = soup.find('div', id='euro').find('strong').text.strip()
            
            return tasa_dolar, tasa_euro
        else:
            print("Error al cargar la página del BCV")
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
    requests.post(url, data=data)

# --- EJECUCIÓN PRINCIPAL ---
dolar, euro = obtener_tasas()

if dolar and euro:
    fecha = datetime.datetime.now().strftime("%d/%m/%Y")
    
    mensaje = (
        f"📢 **Tasa Oficial BCV - {fecha}**\n\n"
        f"🇺🇸 **Dólar:** {dolar} Bs.\n"
        f"🇪🇺 **Euro:** {euro} Bs.\n\n"
        f"🔗 Fuente: Banco Central de Venezuela"
    )
    
    enviar_telegram(mensaje)
    print("Mensaje enviado con éxito.")
else:

    print("No se pudieron obtener las tasas hoy.")
