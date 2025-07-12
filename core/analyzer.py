"""
Analizador principal de algoritmos
Responsable de coordinar el análisis de complejidad temporal
"""

import ast
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path

from .complexity import ComplexityCalculator
from .patterns import PatternDetector
from utils.parser import CodeParser


class AlgorithmAnalyzer:
    """Analizador principal de algoritmos para calcular notación asintótica"""
    
    def __init__(self, use_neural_network: bool = True, model_path: Optional[str] = None):
        self.complexity_calc = ComplexityCalculator()
        self.pattern_detector = PatternDetector()
        self.code_parser = CodeParser()
        self.use_neural_network = use_neural_network
        self.neural_classifier = None
        
        # Cargar modelo de red neuronal si está disponible
        if use_neural_network and model_path:
            try:
                from ml.neural_network import AlgorithmClassifier
                self.neural_classifier = AlgorithmClassifier(model_path)
                print("🧠 Modelo de red neuronal cargado exitosamente")
            except Exception as e:
                print(f"⚠️ No se pudo cargar el modelo de red neuronal: {e}")
                self.use_neural_network = False
        
    def analyze_code(self, code: str, language: str = 'python') -> Dict:
        """
        Analiza código fuente y calcula su complejidad temporal
        
        Args:
            code: Código fuente a analizar
            language: Lenguaje de programación
            
        Returns:
            Diccionario con resultados del análisis
        """
        try:
            # Parsear el código según el lenguaje
            parsed_code = self.code_parser.parse(code, language)
            
            # Detectar patrones de complejidad
            patterns = self.pattern_detector.detect_patterns(code, language)
            
            # Calcular complejidad usando métodos tradicionales
            complexity = self.complexity_calc.calculate_complexity(patterns)
            traditional_notation = self._generate_notation(complexity)
            
            # Predicción de la red neuronal (si está disponible)
            neural_notation = None
            neural_confidence = 0.0
            
            if self.use_neural_network and self.neural_classifier:
                try:
                    neural_notation, neural_confidence = self.neural_classifier.predict(code)
                except Exception as e:
                    print(f"⚠️ Error en predicción de red neuronal: {e}")
            
            # Combinar resultados
            final_notation = self._combine_predictions(
                traditional_notation, neural_notation, neural_confidence
            )
            
            return {
                'success': True,
                'language': language,
                'patterns': patterns,
                'complexity': complexity,
                'notation': final_notation,
                'traditional_notation': traditional_notation,
                'neural_notation': neural_notation,
                'neural_confidence': neural_confidence,
                'explanation': self._generate_explanation(
                    patterns, complexity, final_notation, 
                    traditional_notation, neural_notation, neural_confidence
                )
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'language': language
            }
    
    def analyze_file(self, file_path: str, language: str = 'python') -> Dict:
        """
        Analiza un archivo de código fuente
        
        Args:
            file_path: Ruta al archivo
            language: Lenguaje de programación
            
        Returns:
            Diccionario con resultados del análisis
        """
        try:
            path_obj = Path(file_path)
            if not path_obj.exists():
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
                
            with open(path_obj, 'r', encoding='utf-8') as f:
                code = f.read()
                
            return self.analyze_code(code, language)
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_path': str(file_path),
                'language': language
            }
    
    def _combine_predictions(self, traditional: str, neural: Optional[str], 
                           confidence: float) -> str:
        """Combina predicciones tradicionales y de red neuronal"""
        if not neural or confidence < 0.7:
            # Si la red neuronal no está disponible o tiene baja confianza,
            # usar predicción tradicional
            return traditional
        
        # Si la confianza es alta, usar predicción de red neuronal
        if confidence > 0.9:
            return neural
        
        # Si la confianza es media, verificar si coinciden
        if traditional == neural:
            return traditional
        else:
            # En caso de conflicto, usar la predicción tradicional
            # pero marcar la discrepancia
            return traditional
    
    def _generate_notation(self, complexity: Dict) -> str:
        """Genera la notación asintótica basada en la complejidad calculada"""
        dominant_term = complexity.get('dominant_term', 'O(1)')
        
        # Mapear términos a notaciones estándar
        notation_map = {
            'O(1)': 'O(1)',
            'O(log n)': 'O(log n)',
            'O(n)': 'O(n)',
            'O(n log n)': 'O(n log n)',
            'O(n²)': 'O(n²)',
            'O(n³)': 'O(n³)',
            'O(2ⁿ)': 'O(2ⁿ)',
            'O(n!)': 'O(n!)'
        }
        
        return notation_map.get(dominant_term, dominant_term) or 'O(1)'
    
    def _generate_explanation(self, patterns: List, complexity: Dict, 
                            final_notation: str, traditional_notation: str,
                            neural_notation: Optional[str], neural_confidence: float) -> str:
        """Genera una explicación detallada del análisis"""
        explanation = f"El algoritmo tiene una complejidad temporal de {final_notation}.\n\n"
        
        # Explicación de métodos tradicionales
        explanation += "📊 ANÁLISIS TRADICIONAL:\n"
        explanation += f"• Notación calculada: {traditional_notation}\n"
        
        if patterns:
            explanation += "• Patrones detectados:\n"
            for pattern in patterns:
                explanation += f"  - {pattern['type']}: {pattern['description']}\n"
        else:
            explanation += "• No se detectaron patrones específicos\n"
        
        explanation += f"• Término dominante: {complexity.get('dominant_term', 'O(1)')}\n"
        explanation += f"• Complejidad total: {complexity.get('total_complexity', 'O(1)')}\n\n"
        
        # Explicación de red neuronal
        if self.use_neural_network and neural_notation:
            explanation += "🧠 ANÁLISIS DE RED NEURONAL:\n"
            explanation += f"• Notación predicha: {neural_notation}\n"
            explanation += f"• Confianza: {neural_confidence:.2%}\n"
            
            if traditional_notation != neural_notation:
                explanation += "• ⚠️ Discrepancia entre métodos detectada\n"
            else:
                explanation += "• ✅ Coincidencia entre métodos\n"
            
            explanation += "\n"
        
        # Nota sobre el método final
        if self.use_neural_network and neural_notation and neural_confidence > 0.7:
            if traditional_notation == neural_notation:
                explanation += "✅ RESULTADO FINAL: Ambos métodos coinciden en la predicción.\n"
            else:
                explanation += "🤖 RESULTADO FINAL: Basado en análisis tradicional (red neuronal en conflicto).\n"
        else:
            explanation += "📈 RESULTADO FINAL: Basado en análisis tradicional.\n"
        
        return explanation
    
    def get_supported_languages(self) -> List[str]:
        """Retorna la lista de lenguajes soportados"""
        return ['python', 'javascript', 'java', 'cpp']
    
    def get_complexity_examples(self) -> Dict[str, str]:
        """Retorna ejemplos de algoritmos con sus complejidades"""
        return {
            'O(1)': 'Acceso directo a array, operaciones aritméticas',
            'O(log n)': 'Búsqueda binaria, algoritmos de división y conquista',
            'O(n)': 'Búsqueda lineal, recorrido de array',
            'O(n log n)': 'Merge sort, Quick sort, Heap sort',
            'O(n²)': 'Bubble sort, Selection sort, algoritmos con bucles anidados',
            'O(n³)': 'Multiplicación de matrices, algoritmos con tres bucles anidados',
            'O(2ⁿ)': 'Fibonacci recursivo, algoritmos de fuerza bruta',
            'O(n!)': 'Permutaciones, algoritmos de backtracking'
        }
    
    def enable_neural_network(self, model_path: str):
        """Habilita el uso de la red neuronal"""
        try:
            from ml.neural_network import AlgorithmClassifier
            self.neural_classifier = AlgorithmClassifier(model_path)
            self.use_neural_network = True
            print("🧠 Red neuronal habilitada exitosamente")
        except Exception as e:
            print(f"❌ Error al habilitar red neuronal: {e}")
            self.use_neural_network = False
    
    def disable_neural_network(self):
        """Deshabilita el uso de la red neuronal"""
        self.use_neural_network = False
        self.neural_classifier = None
        print("📊 Red neuronal deshabilitada, usando solo análisis tradicional") 