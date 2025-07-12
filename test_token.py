#!/usr/bin/env python3
"""
Script simple para probar el token de Telegram
"""

import os
import asyncio
from telegram import Bot
from telegram.error import InvalidToken

def test_token():
    """Prueba el token del bot"""
    # Leer token del archivo .env
    try:
        with open('.env', 'r') as f:
            token = None
            for line in f:
                if line.startswith('TELEGRAM_BOT_TOKEN='):
                    token = line.split('=')[1].strip()
                    break
            if not token:
                print("❌ No se encontró el token en .env")
                return False
    except FileNotFoundError:
        print("❌ No se encontró el archivo .env")
        return False
    
    print(f"🔑 Token encontrado: {token[:20]}...")
    
    async def test_connection():
        try:
            bot = Bot(token)
            me = await bot.get_me()
            print(f"✅ Conexión exitosa!")
            print(f"🤖 Nombre del bot: {me.first_name}")
            print(f"👤 Username: @{me.username}")
            print(f"🆔 ID del bot: {me.id}")
            await bot.close()
            return True
        except InvalidToken:
            print("❌ Token inválido")
            return False
        except Exception as e:
            if "Unauthorized" in str(e):
                print("❌ Token no autorizado")
            else:
                print(f"❌ Error: {e}")
            return False
    
    return asyncio.run(test_connection())

if __name__ == "__main__":
    print("🧪 PROBANDO TOKEN DE TELEGRAM")
    print("=" * 40)
    test_token() 