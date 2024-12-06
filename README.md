# jc000001-lotify - Bot de Monitoreo de Lotes de TIE para Telegram 🚀

Este bot de Telegram monitorea los lotes publicados en [Extranjería Murcia](https://www.extranjeriamurcia.com/lotes-recibidos) para una comisaría específica y envía notificaciones. Si el lote alcanza o supera el objetivo definido, envía alertas intensivas hasta que confirmes haberlo leído.

## Características ✨
- Notificaciones regulares cada 8 horas si no se cumple el objetivo.
- Notificaciones intensivas cada 5 minutos cuando se alcanza el objetivo.
- Mensajes personalizados con emojis para facilitar la comunicación.

## Requisitos 🛠️

- Python 3.10 o superior
- Cuenta en [Telegram](https://telegram.org) y un bot configurado con `@BotFather`
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) (si despliegas en Heroku)

## Instalación y Configuración ⚙️

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

### 2. Crear un entorno virtual (opcional)
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en el directorio raíz con las siguientes variables:
```env
TARGET_LOT=220
TARGET_COMISARIA=COMISARÍA DE LORCA
TELEGRAM_BOT_TOKEN=tu_telegram_bot_token
TELEGRAM_CHAT_ID=tu_chat_id
```

### 5. Ejecutar localmente
Ejecuta el bot con:
```bash
python bot.py
```

## Despliegue en Heroku ☁️

### 1. Crear una aplicación en Heroku
1. Ve a [Heroku](https://www.heroku.com/) e inicia sesión.
2. Crea una nueva aplicación.

### 2. Subir el proyecto
Asegúrate de que tu repositorio esté configurado correctamente:
```bash
git init
git add .
git commit -m "Primera versión del bot"
heroku git:remote -a nombre-de-tu-aplicacion
git push heroku main
```

### 3. Configurar variables de entorno en Heroku
En la pestaña **Settings** de tu aplicación en Heroku, agrega las variables de entorno desde el archivo `.env`.

### 4. Verificar que funciona
Activa el dyno `worker` en la pestaña **Resources** y revisa los logs para confirmar que el bot se está ejecutando.

## Estructura del proyecto 📂
```
bot/
├── bot.py                 # Código principal del bot
├── requirements.txt       # Dependencias del proyecto
├── runtime.txt            # Versión de Python para Heroku
├── Procfile               # Archivo de configuración para Heroku
└── .env                   # Variables de entorno (no se sube al repositorio)
```

## Contribuir 🛠️
1. Haz un fork del proyecto.
2. Crea una rama nueva: `git checkout -b feature/nueva-funcionalidad`.
3. Realiza tus cambios y haz un commit: `git commit -m "Agregar nueva funcionalidad"`.
4. Envía tus cambios: `git push origin feature/nueva-funcionalidad`.
5. Crea un pull request.

## Licencia 📜
Este proyecto está bajo la Licencia MIT. Puedes ver más detalles en el archivo [LICENSE](LICENSE).

## Contacto 📧
Cualquier duda o sugerencia, no dudes en contactarme. 😊
