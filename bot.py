import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from twilio.rest import Client

# Cargar variables de entorno
load_dotenv()
TARGET_LOT = int(os.getenv("TARGET_LOT"))
TARGET_COMISARIA = os.getenv("TARGET_COMISARIA")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")

# Configurar cliente de Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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

def send_whatsapp_notification(comisaria, current_lot):
    """Envía una notificación por WhatsApp."""
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        body=(
            f"El lote actual para {comisaria} es {current_lot}. "
            f"Ha alcanzado o superado el objetivo ({TARGET_LOT})."
        ),
        to=WHATSAPP_TO
    )
    print(f"Mensaje enviado: {message.sid}")

def main():
    """Ejecuta el bot en un bucle."""
    print(f"Iniciando el bot para {TARGET_COMISARIA}...")
    while True:
        try:
            current_lot = get_current_lot(TARGET_COMISARIA)
            if current_lot:
                print(f"Lote actual para {TARGET_COMISARIA}: {current_lot}")
                if current_lot >= TARGET_LOT:
                    send_whatsapp_notification(TARGET_COMISARIA, current_lot)
                    break
            else:
                print("No se pudo obtener el lote actual.")
        except Exception as e:
            print(f"Error: {e}")
        
        # Esperar 8 horas antes de verificar nuevamente
        time.sleep(28800)

if __name__ == "__main__":
    main()
