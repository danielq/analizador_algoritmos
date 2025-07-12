#!/usr/bin/env python3
"""
Analizador de Algoritmos - Calculadora de Notación Asintótica
Punto de entrada principal de la aplicación
"""

import sys
import argparse
from pathlib import Path

# Agregar el directorio actual al path para imports
sys.path.append(str(Path(__file__).parent))

from core.analyzer import AlgorithmAnalyzer
from gui.main_window import AlgorithmAnalyzerGUI
from cli.commands import CLIHandler

# Importar el bot de Telegram
from telegram_bot import run_telegram_bot


def main():
    """Función principal que maneja los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description="Analizador de Algoritmos - Calculadora de Notación Asintótica",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --gui                    # Abrir interfaz gráfica
  python main.py --file algoritmo.py     # Analizar archivo
  python main.py --code "for i in range(n): print(i)"  # Analizar código directo
  python main.py --telegram-bot          # Ejecutar chatbot de Telegram
        """
    )
    
    # Argumentos mutuamente excluyentes
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gui', action='store_true', 
                      help='Abrir interfaz gráfica')
    group.add_argument('--file', type=str, 
                      help='Archivo con algoritmo a analizar')
    group.add_argument('--code', type=str, 
                      help='Código directo a analizar')
    group.add_argument('--telegram-bot', action='store_true',
                      help='Ejecutar el chatbot de Telegram')
    
    # Argumentos opcionales
    parser.add_argument('--language', '-l', type=str, default='python',
                      choices=['python', 'javascript', 'java', 'cpp'],
                      help='Lenguaje del código (default: python)')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Mostrar información detallada')
    parser.add_argument('--output', '-o', type=str,
                      help='Archivo de salida para resultados')
    
    args = parser.parse_args()
    
    try:
        if args.gui:
            # Lanzar interfaz gráfica
            app = AlgorithmAnalyzerGUI()
            app.run()
        elif args.telegram_bot:
            # Lanzar el bot de Telegram
            run_telegram_bot()
        else:
            # Usar interfaz de línea de comandos
            cli = CLIHandler()
            
            if args.file:
                cli.analyze_file(args.file, args.language, args.verbose, args.output)
            elif args.code:
                cli.analyze_code(args.code, args.language, args.verbose, args.output)
                
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 