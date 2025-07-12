"""
Calculador de complejidad temporal para algoritmos
"""

from typing import Dict, List, Tuple, Optional
import re


class ComplexityCalculator:
    """Calcula la complejidad temporal de algoritmos basado en patrones detectados"""
    
    def __init__(self):
        self.complexity_patterns = {
            'constant': {'notation': 'O(1)', 'weight': 1},
            'logarithmic': {'notation': 'O(log n)', 'weight': 2},
            'linear': {'notation': 'O(n)', 'weight': 3},
            'linearithmic': {'notation': 'O(n log n)', 'weight': 4},
            'quadratic': {'notation': 'O(n²)', 'weight': 5},
            'cubic': {'notation': 'O(n³)', 'weight': 6},
            'exponential': {'notation': 'O(2ⁿ)', 'weight': 7},
            'factorial': {'notation': 'O(n!)', 'weight': 8}
        }
    
    def calculate_complexity(self, patterns: List[Dict]) -> Dict:
        """
        Calcula la complejidad temporal basada en los patrones detectados
        
        Args:
            patterns: Lista de patrones detectados en el código
            
        Returns:
            Diccionario con información de complejidad
        """
        if not patterns:
            return {
                'dominant_term': 'O(1)',
                'total_complexity': 'O(1)',
                'analysis': 'No se detectaron patrones de complejidad'
            }
        
        # Analizar cada patrón
        complexity_terms = []
        for pattern in patterns:
            term = self._analyze_pattern_complexity(pattern)
            if term:
                complexity_terms.append(term)
        
        if not complexity_terms:
            return {
                'dominant_term': 'O(1)',
                'total_complexity': 'O(1)',
                'analysis': 'No se pudo determinar la complejidad'
            }
        
        # Encontrar el término dominante
        dominant_term = self._find_dominant_term(complexity_terms)
        
        # Calcular complejidad total
        total_complexity = self._calculate_total_complexity(complexity_terms)
        
        return {
            'dominant_term': dominant_term,
            'total_complexity': total_complexity,
            'terms': complexity_terms,
            'analysis': self._generate_complexity_analysis(complexity_terms, dominant_term)
        }
    
    def _analyze_pattern_complexity(self, pattern: Dict) -> Optional[Dict]:
        """Analiza la complejidad de un patrón específico"""
        pattern_type = pattern.get('type', '')
        description = pattern.get('description', '')
        
        # Detectar bucles anidados
        if 'nested_loop' in pattern_type:
            nesting_level = self._count_nesting_level(description)
            if nesting_level == 1:
                return {'type': 'linear', 'notation': 'O(n)', 'description': description}
            elif nesting_level == 2:
                return {'type': 'quadratic', 'notation': 'O(n²)', 'description': description}
            elif nesting_level == 3:
                return {'type': 'cubic', 'notation': 'O(n³)', 'description': description}
            else:
                return {'type': 'polynomial', 'notation': f'O(n^{nesting_level})', 'description': description}
        
        # Detectar recursión
        elif 'recursion' in pattern_type:
            if 'fibonacci' in description.lower() or 'exponential' in description.lower():
                return {'type': 'exponential', 'notation': 'O(2ⁿ)', 'description': description}
            elif 'factorial' in description.lower():
                return {'type': 'factorial', 'notation': 'O(n!)', 'description': description}
            else:
                return {'type': 'recursive', 'notation': 'O(2ⁿ)', 'description': description}
        
        # Detectar búsqueda binaria
        elif 'binary_search' in pattern_type:
            return {'type': 'logarithmic', 'notation': 'O(log n)', 'description': description}
        
        # Detectar algoritmos de ordenamiento
        elif 'sorting' in pattern_type:
            if 'merge' in description.lower() or 'quick' in description.lower() or 'heap' in description.lower():
                return {'type': 'linearithmic', 'notation': 'O(n log n)', 'description': description}
            elif 'bubble' in description.lower() or 'selection' in description.lower() or 'insertion' in description.lower():
                return {'type': 'quadratic', 'notation': 'O(n²)', 'description': description}
        
        # Detectar bucle simple
        elif 'simple_loop' in pattern_type:
            return {'type': 'linear', 'notation': 'O(n)', 'description': description}
        
        # Detectar operaciones constantes
        elif 'constant' in pattern_type:
            return {'type': 'constant', 'notation': 'O(1)', 'description': description}
        
        return None
    
    def _count_nesting_level(self, description: str) -> int:
        """Cuenta el nivel de anidamiento de bucles"""
        # Si la descripción menciona bucles anidados, contar las líneas
        if 'anidados' in description.lower():
            # Extraer números de línea de la descripción
            line_numbers = re.findall(r'\d+', description)
            if len(line_numbers) >= 2:
                # Si hay múltiples líneas mencionadas, es al menos 2 bucles anidados
                return 2
            else:
                return 2  # Por defecto para bucles anidados
        
        # Buscar patrones de bucles anidados en el texto
        nested_patterns = [
            r'for.*for.*for',  # 3 bucles anidados
            r'for.*for',       # 2 bucles anidados
            r'while.*while.*while',  # 3 whiles anidados
            r'while.*while',   # 2 whiles anidados
        ]
        
        for i, pattern in enumerate(nested_patterns, 1):
            if re.search(pattern, description, re.IGNORECASE):
                return i + 1
        
        return 1  # Por defecto, un bucle
    
    def _find_dominant_term(self, terms: List[Dict]) -> str:
        """Encuentra el término dominante en la complejidad"""
        if not terms:
            return 'O(1)'
        
        # Ordenar por peso de complejidad
        sorted_terms = sorted(terms, key=lambda x: self.complexity_patterns.get(x['type'], {}).get('weight', 0), reverse=True)
        
        return sorted_terms[0]['notation']
    
    def _calculate_total_complexity(self, terms: List[Dict]) -> str:
        """Calcula la complejidad total combinando todos los términos"""
        if not terms:
            return 'O(1)'
        
        # Si solo hay un término, es la complejidad total
        if len(terms) == 1:
            return terms[0]['notation']
        
        # Si hay múltiples términos, tomar el dominante
        return self._find_dominant_term(terms)
    
    def _generate_complexity_analysis(self, terms: List[Dict], dominant_term: str) -> str:
        """Genera un análisis detallado de la complejidad"""
        analysis = f"Complejidad dominante: {dominant_term}\n"
        
        if len(terms) > 1:
            analysis += f"Se detectaron {len(terms)} patrones de complejidad:\n"
            for term in terms:
                analysis += f"• {term['notation']}: {term['description']}\n"
        else:
            analysis += f"Patrón detectado: {terms[0]['description']}"
        
        return analysis
    
    def get_complexity_guide(self) -> Dict[str, str]:
        """Retorna una guía de complejidades comunes"""
        return {
            'O(1)': 'Operaciones constantes: acceso a array, operaciones aritméticas',
            'O(log n)': 'Búsqueda binaria, algoritmos de división y conquista',
            'O(n)': 'Búsqueda lineal, recorrido de array, algoritmos lineales',
            'O(n log n)': 'Algoritmos de ordenamiento eficientes: Merge Sort, Quick Sort',
            'O(n²)': 'Algoritmos con bucles anidados: Bubble Sort, Selection Sort',
            'O(n³)': 'Algoritmos con tres bucles anidados: multiplicación de matrices',
            'O(2ⁿ)': 'Algoritmos exponenciales: Fibonacci recursivo, fuerza bruta',
            'O(n!)': 'Algoritmos factoriales: permutaciones, backtracking'
        } 