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

# Verificar que las variables están correctamente cargadas
print(f"Target Lot: {TARGET_LOT}")
print(f"Comisaría: {TARGET_COMISARIA}")

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

def send_telegram_notification(message):
    """Envía una notificación por Telegram."""
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
    """Ejecuta el bot con notificaciones regulares e intensivas."""
    print(f"Iniciando el bot para {TARGET_COMISARIA}...")
    notified_goal = False  # Notificación de objetivo cumplido
    notified_update = False  # Notificación de actualización regular

    while True:
        try:
            # Obtener el lote actual
            current_lot = get_current_lot(TARGET_COMISARIA)
            if current_lot:
                print(f"Lote actual para {TARGET_COMISARIA}: {current_lot}")

                if current_lot >= TARGET_LOT:
                    # Notificar intensivamente cada 5 minutos si se cumple el objetivo
                    message = (
                        f"🎉 *¡Buenas noticias!* 🎉\n\n"
                        f"El lote actual para *{TARGET_COMISARIA}* es `{current_lot}`.\n"
                        f"🎯 ¡Ha alcanzado o superado el objetivo (`{TARGET_LOT}`)!\n\n"
                        f"Por favor, confirma que has leído este mensaje."
                    )
                    send_telegram_notification(message)
                    notified_goal = True
                    notified_update = False  # Restablecer actualizaciones regulares
                    time.sleep(300)  # 5 minutos para la siguiente notificación
                else:
                    # Notificaciones regulares cada 8 horas si no se cumple el objetivo
                    if not notified_update:
                        message = (
                            f"🌐 *Actualización de lotes*\n\n"
                            f"El lote actual para *{TARGET_COMISARIA}* es `{current_lot}`.\n"
                            f"❌ Todavía no se ha alcanzado el objetivo (`{TARGET_LOT}`).\n\n"
                            f"Seguiremos monitoreando y te avisaremos cuando esté disponible. 🕒"
                        )
                        send_telegram_notification(message)
                        notified_update = True  # Marcar notificación enviada
                        notified_goal = False  # Restablecer objetivo no cumplido
                    time.sleep(28800)  # 8 horas en segundos
            else:
                print("No se pudo obtener el lote actual. Intentando nuevamente en 8 horas.")
                time.sleep(28800)  # 8 horas en segundos

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(600)  # 10 minutos antes de reintentar en caso de error

if __name__ == "__main__":
    main()
