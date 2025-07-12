"""
Manejador de comandos de línea de comandos para el analizador de algoritmos
"""

import sys
from pathlib import Path
from typing import Optional

from core.analyzer import AlgorithmAnalyzer


class CLIHandler:
    """Manejador de la interfaz de línea de comandos"""
    
    def __init__(self):
        self.analyzer = AlgorithmAnalyzer()
        
    def analyze_file(self, file_path: str, language: str = 'python', 
                    verbose: bool = False, output_file: Optional[str] = None):
        """Analiza un archivo de código"""
        try:
            print(f"🔍 Analizando archivo: {file_path}")
            print(f"📝 Lenguaje: {language}")
            print("-" * 50)
            
            result = self.analyzer.analyze_file(file_path, language)
            self._display_result(result, verbose, output_file)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def analyze_code(self, code: str, language: str = 'python', 
                    verbose: bool = False, output_file: Optional[str] = None):
        """Analiza código directo"""
        try:
            print(f"🔍 Analizando código directo")
            print(f"📝 Lenguaje: {language}")
            print("-" * 50)
            
            result = self.analyzer.analyze_code(code, language)
            self._display_result(result, verbose, output_file)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def _display_result(self, result: dict, verbose: bool, output_file: Optional[str]):
        """Muestra los resultados del análisis"""
        if result.get('success'):
            notation = result.get('notation', 'No determinado')
            explanation = result.get('explanation', '')
            
            output = []
            output.append("✅ ANÁLISIS COMPLETADO")
            output.append("")
            output.append(f"📊 NOTACIÓN ASINTÓTICA: {notation}")
            output.append("")
            output.append("📝 EXPLICACIÓN:")
            output.append(explanation)
            output.append("")
            
            if result.get('patterns') and verbose:
                output.append("🔍 PATRONES DETECTADOS:")
                for pattern in result['patterns']:
                    output.append(f"• {pattern['type']}: {pattern['description']}")
                output.append("")
            
            if verbose and result.get('complexity'):
                complexity = result['complexity']
                output.append("🔬 DETALLES DE COMPLEJIDAD:")
                output.append(f"• Término dominante: {complexity.get('dominant_term', 'O(1)')}")
                output.append(f"• Complejidad total: {complexity.get('total_complexity', 'O(1)')}")
                output.append("")
            
            result_text = "\n".join(output)
            print(result_text)
            
            # Guardar en archivo si se especifica
            if output_file:
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result_text)
                    print(f"💾 Resultados guardados en: {output_file}")
                except Exception as e:
                    print(f"⚠️  No se pudo guardar en archivo: {e}")
        else:
            error_msg = f"❌ ERROR EN EL ANÁLISIS\n\nError: {result.get('error', 'Error desconocido')}"
            print(error_msg)
            
            if output_file:
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(error_msg)
                except Exception as e:
                    print(f"⚠️  No se pudo guardar en archivo: {e}")
    
    def show_help(self):
        """Muestra información de ayuda"""
        help_text = """
🔧 ANALIZADOR DE ALGORITMOS - AYUDA

Uso:
  python main.py --gui                    # Abrir interfaz gráfica
  python main.py --file algoritmo.py     # Analizar archivo
  python main.py --code "for i in range(n): print(i)"  # Analizar código directo

Opciones:
  --language, -l    Lenguaje del código (python, javascript, java, cpp)
  --verbose, -v     Mostrar información detallada
  --output, -o      Archivo de salida para resultados

Ejemplos:
  python main.py --file bubble_sort.py --language python --verbose
  python main.py --code "for i in range(n): for j in range(n): print(i,j)" --output resultado.txt

Lenguajes soportados:
  • Python (.py)
  • JavaScript (.js)
  • Java (.java)
  • C++ (.cpp)
        """
        print(help_text)
    
    def show_examples(self):
        """Muestra ejemplos de algoritmos"""
        examples = self.analyzer.get_complexity_examples()
        
        print("📚 EJEMPLOS DE COMPLEJIDAD TEMPORAL")
        print("=" * 50)
        
        for notation, description in examples.items():
            print(f"\n{notation}:")
            print(f"  {description}")
        
        print("\n" + "=" * 50) 