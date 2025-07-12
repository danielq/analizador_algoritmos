#!/usr/bin/env python3
"""
Chatbot de Telegram para el Analizador de Algoritmos
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from core.analyzer import AlgorithmAnalyzer
import json

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class AlgorithmAnalyzerBot:
    """Bot de Telegram para análisis de algoritmos"""
    
    def __init__(self, token: str):
        self.token = token
        self.analyzer = AlgorithmAnalyzer()
        self.user_sessions = {}  # Para almacenar estado de usuarios
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        if not update.message:
            return
            
        welcome_message = """
🤖 **Analizador de Algoritmos Bot**

¡Hola! Soy tu asistente para analizar la complejidad temporal de algoritmos.

**Comandos disponibles:**
• `/analyze` - Analizar código de algoritmo
• `/help` - Mostrar ayuda
• `/examples` - Ver ejemplos de algoritmos
• `/complexity` - Guía de notaciones asintóticas
• `/about` - Información sobre el bot

**Cómo usar:**
1. Envía `/analyze` seguido de tu código
2. O simplemente envía código directamente
3. El bot te dirá la notación O() del algoritmo

¡Empecemos! 🚀
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Analizar Código", callback_data="analyze")],
            [InlineKeyboardButton("📚 Ejemplos", callback_data="examples")],
            [InlineKeyboardButton("📖 Guía de Complejidad", callback_data="complexity")],
            [InlineKeyboardButton("❓ Ayuda", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        if not update.message:
            return
            
        help_text = """
📖 **Ayuda del Analizador de Algoritmos**

**Comandos principales:**
• `/start` - Iniciar el bot
• `/analyze <código>` - Analizar código específico
• `/examples` - Ver ejemplos de algoritmos
• `/complexity` - Guía de notaciones O()

**Formas de analizar código:**
1. **Comando directo:** `/analyze def bubble_sort(arr): ...`
2. **Envío directo:** Simplemente envía el código
3. **Archivo:** Envía un archivo .py, .js, .java, .cpp

**Lenguajes soportados:**
• Python
• JavaScript
• Java
• C++

**Ejemplo de uso:**
```
/analyze def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

¿Necesitas más ayuda? 🤔
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def examples_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /examples"""
        if not update.message:
            return
            
        examples_text = """
📚 **Ejemplos de Algoritmos**

**O(1) - Constante:**
```python
def get_first(arr):
    return arr[0] if arr else None
```

**O(n) - Lineal:**
```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

**O(n²) - Cuadrático:**
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```

**O(2ⁿ) - Exponencial:**
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**O(n log n) - Linealítmico:**
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

¡Prueba analizando alguno de estos ejemplos! 🧪
        """
        await update.message.reply_text(examples_text, parse_mode='Markdown')
    
    async def complexity_guide(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /complexity"""
        if not update.message:
            return
            
        guide_text = """
📊 **Guía de Notaciones Asintóticas**

**O(1) - Constante**
• Acceso directo a arrays
• Operaciones aritméticas básicas
• Ejemplo: `arr[0]`, `x + y`

**O(log n) - Logarítmica**
• Búsqueda binaria
• Algoritmos de división y conquista
• Ejemplo: `binary_search()`

**O(n) - Lineal**
• Búsqueda lineal
• Recorrido de arrays
• Ejemplo: `for i in range(n):`

**O(n log n) - Linealítmica**
• Merge Sort, Quick Sort, Heap Sort
• Algoritmos de ordenamiento eficientes
• Ejemplo: `sorted(arr)`

**O(n²) - Cuadrática**
• Bubble Sort, Selection Sort
• Bucles anidados
• Ejemplo: `for i in range(n): for j in range(n):`

**O(n³) - Cúbica**
• Multiplicación de matrices
• Tres bucles anidados
• Ejemplo: `for i in range(n): for j in range(n): for k in range(n):`

**O(2ⁿ) - Exponencial**
• Fibonacci recursivo
• Algoritmos de fuerza bruta
• Ejemplo: `def fib(n): return fib(n-1) + fib(n-2)`

**O(n!) - Factorial**
• Permutaciones
• Algoritmos de backtracking
• Ejemplo: generar todas las permutaciones

¡Ahora ya sabes qué significa cada notación! 🎓
        """
        await update.message.reply_text(guide_text, parse_mode='Markdown')
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /analyze"""
        if not update.message:
            return
            
        if not context.args:
            await update.message.reply_text(
                "❌ Por favor, incluye el código a analizar.\n"
                "Ejemplo: `/analyze def bubble_sort(arr): ...`",
                parse_mode='Markdown'
            )
            return
        
        code = ' '.join(context.args)
        await self.analyze_code(update, context, code)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes de texto que contienen código"""
        if not update.message or not update.message.text:
            return
            
        text = update.message.text
        
        # Si el mensaje parece código (contiene palabras clave)
        code_keywords = ['def ', 'function ', 'for ', 'while ', 'if ', 'class ', 'public ', 'int ', 'void ']
        if any(keyword in text for keyword in code_keywords):
            await self.analyze_code(update, context, text)
        else:
            # Mensaje de ayuda si no es código
            await update.message.reply_text(
                "🤖 Envía código de un algoritmo para analizarlo, o usa /help para ver los comandos disponibles."
            )
    
    async def analyze_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE, code: str):
        """Analiza código y envía el resultado"""
        if not update.message:
            return
            
        try:
            # Mostrar mensaje de "analizando..."
            processing_msg = await update.message.reply_text("🔍 Analizando código...")
            
            # Detectar lenguaje
            language = self._detect_language(code)
            
            # Analizar código
            result = self.analyzer.analyze_code(code, language)
            
            # Formatear resultado
            response = self._format_analysis_result(result, code)
            
            # Enviar resultado
            await processing_msg.edit_text(response, parse_mode='Markdown')
            
        except Exception as e:
            error_msg = f"❌ Error al analizar el código:\n{str(e)}"
            await update.message.reply_text(error_msg)
    
    def _detect_language(self, code: str) -> str:
        """Detecta el lenguaje de programación del código"""
        code_lower = code.lower()
        
        if 'def ' in code_lower or 'import ' in code_lower or 'print(' in code_lower:
            return 'python'
        elif 'function ' in code_lower or 'var ' in code_lower or 'console.log' in code_lower:
            return 'javascript'
        elif 'public ' in code_lower or 'class ' in code_lower or 'System.out' in code_lower:
            return 'java'
        elif '#include' in code_lower or 'int main' in code_lower or 'cout' in code_lower:
            return 'cpp'
        else:
            return 'python'  # Por defecto
    
    def _format_analysis_result(self, result: dict, code: str) -> str:
        """Formatea el resultado del análisis para Telegram"""
        if not result.get('success'):
            return f"❌ **Error en el análisis:**\n{result.get('error', 'Error desconocido')}"
        
        notation = result.get('notation', 'No determinado')
        explanation = result.get('explanation', '')
        
        # Limitar el código para mostrar
        code_preview = code[:200] + "..." if len(code) > 200 else code
        
        response = f"""
🔍 **ANÁLISIS COMPLETADO**

📝 **Código analizado:**
```python
{code_preview}
```

📊 **NOTACIÓN ASINTÓTICA:** `{notation}`

📖 **EXPLICACIÓN:**
{explanation}
        """
        
        # Agregar patrones detectados si existen
        if result.get('patterns'):
            response += "\n🔍 **PATRONES DETECTADOS:**\n"
            for pattern in result['patterns'][:5]:  # Limitar a 5 patrones
                response += f"• {pattern['type']}: {pattern['description']}\n"
        
        # Agregar detalles técnicos si existen
        if result.get('complexity'):
            complexity = result['complexity']
            response += f"\n🔬 **DETALLES TÉCNICOS:**\n"
            response += f"• Término dominante: {complexity.get('dominant_term', 'O(1)')}\n"
            response += f"• Complejidad total: {complexity.get('total_complexity', 'O(1)')}\n"
        
        return response
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja callbacks de botones inline"""
        query = update.callback_query
        if not query:
            return
            
        await query.answer()
        
        if query.data == "analyze":
            await query.edit_message_text(
                "📝 Envía el código del algoritmo que quieres analizar.\n"
                "Puedes enviarlo como texto o usar el comando /analyze <código>"
            )
        elif query.data == "examples":
            await self.examples_command(update, context)
        elif query.data == "complexity":
            await self.complexity_guide(update, context)
        elif query.data == "help":
            await self.help_command(update, context)
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /about"""
        if not update.message:
            return
            
        about_text = """
🤖 **Sobre el Analizador de Algoritmos Bot**

**Versión:** 1.0.0
**Desarrollado por:** Tu equipo de desarrollo

**Características:**
• ✅ Análisis de complejidad temporal
• ✅ Soporte para múltiples lenguajes
• ✅ Detección automática de patrones
• ✅ Red neuronal para mejor precisión
• ✅ Interfaz intuitiva de Telegram

**Lenguajes soportados:**
• Python
• JavaScript
• Java
• C++

**Tecnologías utilizadas:**
• Python 3.12
• python-telegram-bot
• TensorFlow/Keras
• Análisis AST

¡Gracias por usar nuestro bot! 🚀
        """
        await update.message.reply_text(about_text, parse_mode='Markdown')
    
    def run(self):
        """Ejecuta el bot"""
        # Crear aplicación
        application = Application.builder().token(self.token).build()
        
        # Agregar handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("analyze", self.analyze_command))
        application.add_handler(CommandHandler("examples", self.examples_command))
        application.add_handler(CommandHandler("complexity", self.complexity_guide))
        application.add_handler(CommandHandler("about", self.about_command))
        
        # Handler para botones inline
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Handler para mensajes de texto
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Iniciar el bot
        print("🤖 Bot iniciado. Presiona Ctrl+C para detener.")
        application.run_polling()


def main():
    """Función principal"""
    # Obtener token del bot desde variable de entorno
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ Error: No se encontró el token del bot.")
        print("Por favor, configura la variable de entorno TELEGRAM_BOT_TOKEN")
        print("\nPara obtener un token:")
        print("1. Habla con @BotFather en Telegram")
        print("2. Crea un nuevo bot con /newbot")
        print("3. Copia el token y ejecuta:")
        print("   export TELEGRAM_BOT_TOKEN='tu_token_aqui'")
        return
    
    # Crear y ejecutar el bot
    bot = AlgorithmAnalyzerBot(token)
    bot.run()


def run_telegram_bot():
    """Lanza el bot de Telegram (wrapper para integración con main.py)"""
    main()


if __name__ == "__main__":
    main() 