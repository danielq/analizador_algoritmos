#!/usr/bin/env python3
"""
Script de configuración para el bot de Telegram
"""

import os
import sys
from pathlib import Path

def setup_bot():
    """Configura el bot de Telegram"""
    print("🤖 CONFIGURACIÓN DEL BOT DE TELEGRAM")
    print("=" * 50)
    
    # Verificar si ya existe el token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if token:
        print(f"✅ Token encontrado: {token[:10]}...")
        choice = input("¿Quieres usar este token? (s/n): ").lower()
        if choice != 's':
            token = None
    
    if not token:
        print("\n📋 Para crear un bot de Telegram:")
        print("1. Abre Telegram y busca @BotFather")
        print("2. Envía /newbot")
        print("3. Sigue las instrucciones para crear tu bot")
        print("4. Copia el token que te proporciona")
        print("\n🔑 Ingresa tu token del bot:")
        token = input("Token: ").strip()
        
        if not token:
            print("❌ Token no válido. Saliendo...")
            return False
    
    # Guardar token en archivo .env
    env_file = Path(".env")
    env_content = f"TELEGRAM_BOT_TOKEN={token}\n"
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Token guardado en {env_file}")
    
    # Configurar variable de entorno para esta sesión
    os.environ['TELEGRAM_BOT_TOKEN'] = token
    
    print("\n🎉 Configuración completada!")
    print("Para ejecutar el bot:")
    print("  python3 telegram_bot.py")
    
    return True

def test_bot():
    """Prueba la conexión del bot"""
    print("\n🧪 PROBANDO CONEXIÓN DEL BOT")
    print("=" * 30)
    
    try:
        from telegram import Bot
        import asyncio
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            print("❌ No se encontró el token")
            return False
        
        async def test_connection():
            bot = Bot(token)
            me = await bot.get_me()
            print(f"✅ Conexión exitosa!")
            print(f"🤖 Nombre del bot: {me.first_name}")
            print(f"👤 Username: @{me.username}")
            print(f"🆔 ID del bot: {me.id}")
            await bot.close()
        
        asyncio.run(test_connection())
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 CONFIGURADOR DEL BOT DE TELEGRAM")
    print("=" * 50)
    
    # Verificar dependencias
    try:
        import telegram
        print("✅ python-telegram-bot instalado")
    except ImportError:
        print("❌ python-telegram-bot no está instalado")
        print("Ejecuta: pip install python-telegram-bot")
        return
    
    # Configurar bot
    if setup_bot():
        # Probar conexión
        if test_bot():
            print("\n🎉 ¡Todo listo! Puedes ejecutar el bot con:")
            print("  python3 telegram_bot.py")
        else:
            print("\n❌ Error en la conexión. Verifica el token.")
    else:
        print("\n❌ Configuración fallida.")

if __name__ == "__main__":
    main() 