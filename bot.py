import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TARGET_LOT = int(os.getenv("TARGET_LOT"))
TARGET_COMISARIA = os.getenv("TARGET_COMISARIA")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# URL a monitorear
URL = "https://www.extranjeriamurcia.com/lotes-recibidos"

def get_current_lot(comisaria):
    """Obtiene el lote actual de la comisaría especificada."""
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar el texto que contiene el nombre de la comisaría
    element = soup.find(string=lambda text: text and comisaria in text)
    if element:
        # Extraer el número del lote
        lot_text = element.split("HASTA LOTE ")[-1].split(" /")[0]
        return int(lot_text)
    return None

def send_telegram_notification(comisaria, current_lot):
    """Envía una notificación por Telegram."""
    message = (
        f"📢 *Actualización de lotes*\n\n"
        f"El lote actual para *{comisaria}* es `{current_lot}`.\n"
        f"Ha alcanzado o superado el objetivo (`{TARGET_LOT}`)."
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Mensaje enviado por Telegram.")
    else:
        print(f"Error al enviar mensaje: {response.status_code}, {response.text}")

def main():
    """Ejecuta el bot en un bucle."""
    print(f"Iniciando el bot para {TARGET_COMISARIA}...")
    while True:
        try:
            current_lot = get_current_lot(TARGET_COMISARIA)
            if current_lot:
                print(f"Lote actual para {TARGET_COMISARIA}: {current_lot}")
                if current_lot >= TARGET_LOT:
                    send_telegram_notification(TARGET_COMISARIA, current_lot)
                    break
            else:
                print("No se pudo obtener el lote actual.")
        except Exception as e:
            print(f"Error: {e}")
        
        # Esperar 8 horas antes de verificar nuevamente
        time.sleep(28800)

if __name__ == "__main__":
    main()
