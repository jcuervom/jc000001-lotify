import os
import requests
from dotenv import load_dotenv
import time

# Cargar variables de entorno
load_dotenv()

# Leer las variables
target_lot = os.getenv("TARGET_LOT")
target_comisaria = os.getenv("TARGET_COMISARIA")
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Debug: Verificar que las variables de entorno se están leyendo correctamente
print(f"Target Lot: {target_lot}")
print(f"Comisaría: {target_comisaria}")
print(f"Telegram Bot Token: {telegram_bot_token}")
print(f"Telegram Chat ID: {telegram_chat_id}")

if not target_lot or not target_comisaria or not telegram_bot_token or not telegram_chat_id:
    print("Error: Algunas variables de entorno no están configuradas correctamente.")
    exit()

# Función para enviar un mensaje a Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Mensaje enviado correctamente.")
        else:
            print(f"Error al enviar mensaje: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error al intentar enviar el mensaje a Telegram: {e}")

# Función para verificar el lote y enviar notificación si es necesario
def check_lote():
    print("Iniciando la verificación del lote...")

    # Aquí va la lógica para obtener los datos del sitio web y verificar el lote
    # Ejemplo de datos simulados:
    # Si el lote en la página web es igual o mayor al target, enviamos el mensaje
    current_lote = 220  # Aquí deberías poner el valor real obtenido de la página web

    print(f"Lote actual: {current_lote}")

    if current_lote >= int(target_lot):
        message = f"¡ALERTA! El lote {current_lote} ha alcanzado el objetivo de {target_lot}.\n¡Es hora de actuar!"
        send_telegram_message(message)
    else:
        print("El lote no ha alcanzado el objetivo, revisando nuevamente...")
        message = "Aún no está disponible el lote que estamos esperando. Seguimos monitoreando..."
        send_telegram_message(message)

# Revisión periódica cada 8 horas
while True:
    check_lote()
    time.sleep(28800)  # 8 horas en segundos
