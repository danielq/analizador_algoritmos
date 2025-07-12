#!/usr/bin/env python3
"""
Configuración para el bot de Telegram
"""

import os
from pathlib import Path

# Configuración del bot
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Configuración de logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Configuración del analizador
DEFAULT_LANGUAGE = 'python'
SUPPORTED_LANGUAGES = ['python', 'javascript', 'java', 'cpp']

# Configuración de mensajes
MAX_CODE_LENGTH = 2000  # Longitud máxima del código para mostrar
MAX_PATTERNS_SHOW = 5   # Máximo número de patrones a mostrar

# Configuración de archivos
MODEL_PATH = "models/algorithm_classifier"
DATASET_PATH = "ml/dataset_generator.py"

# Configuración de respuestas
RESPONSE_TEMPLATES = {
    'welcome': """
🤖 **Analizador de Algoritmos Bot**

¡Hola! Soy tu asistente para analizar la complejidad temporal de algoritmos.

**Comandos disponibles:**
• `/analyze` - Analizar código de algoritmo
• `/help` - Mostrar ayuda
• `/examples` - Ver ejemplos de algoritmos
• `/complexity` - Guía de notaciones asintóticas
• `/about` - Información sobre el bot

¡Empecemos! 🚀
    """,
    
    'error': "❌ **Error:** {error}",
    'processing': "🔍 Analizando código...",
    'no_code': "❌ Por favor, incluye código para analizar.",
    'help': "🤖 Envía código de un algoritmo para analizarlo, o usa /help para ver los comandos disponibles."
} 