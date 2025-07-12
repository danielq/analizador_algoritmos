# 🚀 Guía de Despliegue - Analizador de Algoritmos

## Opciones de Despliegue

### 1. **Railway (Recomendado - Gratis)**

**Ventajas:**
- ✅ Gratis para proyectos personales
- ✅ Despliegue automático desde GitHub
- ✅ SSL automático
- ✅ Muy fácil de usar

**Pasos:**
1. Ve a [railway.app](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Configura la variable de entorno `TELEGRAM_BOT_TOKEN`
4. ¡Listo! Se despliega automáticamente

**Comando rápido:**
```bash
./deploy.sh
# Selecciona opción 1
```

### 2. **Heroku**

**Ventajas:**
- ✅ Confiable y estable
- ✅ Buena documentación
- ✅ Integración con GitHub

**Pasos:**
1. Instala Heroku CLI
2. Ejecuta: `./deploy.sh` y selecciona opción 2
3. O manualmente:
```bash
heroku create tu-app-name
heroku config:set TELEGRAM_BOT_TOKEN=tu_token
git push heroku main
```

### 3. **Docker (Local o VPS)**

**Para desarrollo local:**
```bash
docker-compose up -d
```

**Para VPS:**
1. Sube el código a tu servidor
2. Instala Docker: `curl -fsSL https://get.docker.com | sh`
3. Ejecuta: `docker-compose up -d`

### 4. **VPS Tradicional**

**Pasos:**
1. Conecta a tu VPS via SSH
2. Instala Python 3.12 y pip
3. Clona el repositorio
4. Instala dependencias: `pip install -r requirements.txt`
5. Configura el token: `export TELEGRAM_BOT_TOKEN=tu_token`
6. Ejecuta: `python main.py --telegram-bot`

## Configuración del Bot de Telegram

### 1. Crear el Bot
1. Habla con [@BotFather](https://t.me/BotFather) en Telegram
2. Envía `/newbot`
3. Sigue las instrucciones
4. Copia el token que te da

### 2. Configurar el Token

**En Railway/Heroku:**
- Ve a las variables de entorno de tu app
- Agrega: `TELEGRAM_BOT_TOKEN=tu_token_aqui`

**En Docker:**
```bash
export TELEGRAM_BOT_TOKEN=tu_token_aqui
docker-compose up -d
```

**En VPS:**
```bash
export TELEGRAM_BOT_TOKEN=tu_token_aqui
python main.py --telegram-bot
```

## Verificación del Despliegue

### 1. Verificar que el Bot Funciona
1. Busca tu bot en Telegram
2. Envía `/start`
3. Deberías recibir el mensaje de bienvenida

### 2. Probar Análisis
Envía este código al bot:
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```

Deberías recibir: `O(n²)`

## Monitoreo y Logs

### Railway
- Ve a tu proyecto en Railway
- Sección "Deployments" para ver logs

### Heroku
```bash
heroku logs --tail
```

### Docker
```bash
docker-compose logs -f
```

### VPS
```bash
# Si usas systemd
sudo journalctl -u tu-servicio -f

# Si usas screen/tmux
# Los logs aparecen en la terminal
```

## Troubleshooting

### Error: "No se encontró el token"
- Verifica que `TELEGRAM_BOT_TOKEN` esté configurado
- Reinicia la aplicación después de configurar

### Error: "Module not found"
- Verifica que `requirements.txt` esté actualizado
- Reinstala dependencias: `pip install -r requirements.txt`

### Bot no responde
- Verifica que el bot esté ejecutándose
- Revisa los logs para errores
- Asegúrate de que el token sea correcto

## Costos Estimados

| Plataforma | Plan Gratuito | Plan Pago |
|------------|---------------|-----------|
| Railway    | ✅ $0/mes      | $5/mes    |
| Heroku     | ❌ No disponible | $7/mes   |
| VPS        | $5-10/mes     | $5-50/mes |
| Docker     | $0 (local)    | $0 (local) |

## Recomendación Final

**Para principiantes:** Railway
**Para producción:** Heroku o VPS
**Para desarrollo:** Docker local 