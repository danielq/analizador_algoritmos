"""
Detector de patrones en algoritmos para análisis de complejidad
"""

import re
import ast
from typing import Dict, List, Optional


class PatternDetector:
    """Detecta patrones en código fuente que indican complejidad temporal"""
    
    def __init__(self):
        self.patterns = {
            'python': self._get_python_patterns(),
            'javascript': self._get_javascript_patterns(),
            'java': self._get_java_patterns(),
            'cpp': self._get_cpp_patterns()
        }
    
    def detect_patterns(self, code: str, language: str = 'python') -> List[Dict]:
        """
        Detecta patrones en el código fuente
        
        Args:
            code: Código fuente a analizar
            language: Lenguaje de programación
            
        Returns:
            Lista de patrones detectados
        """
        patterns = []
        
        if language == 'python':
            patterns.extend(self._detect_python_patterns(code))
        elif language == 'javascript':
            patterns.extend(self._detect_javascript_patterns(code))
        elif language == 'java':
            patterns.extend(self._detect_java_patterns(code))
        elif language == 'cpp':
            patterns.extend(self._detect_cpp_patterns(code))
        
        return patterns
    
    def _get_python_patterns(self) -> Dict:
        """Patrones específicos para Python"""
        return {
            'nested_loops': [
                r'for\s+\w+\s+in\s+.*:\s*\n.*for\s+\w+\s+in\s+.*:',
                r'while\s+.*:\s*\n.*while\s+.*:'
            ],
            'simple_loops': [
                r'for\s+\w+\s+in\s+.*:',
                r'while\s+.*:'
            ],
            'recursion': [
                r'def\s+\w+\s*\(.*\):\s*\n.*\w+\s*\(.*\)',
                r'return\s+\w+\s*\(.*\)'
            ],
            'sorting': [
                r'sort\s*\(',
                r'sorted\s*\(',
                r'\.sort\s*\('
            ],
            'binary_search': [
                r'//\s*2',
                r'\/\s*2',
                r'mid\s*=',
                r'middle\s*='
            ]
        }
    
    def _get_javascript_patterns(self) -> Dict:
        """Patrones específicos para JavaScript"""
        return {
            'nested_loops': [
                r'for\s*\(.*\)\s*{\s*\n.*for\s*\(.*\)\s*{',
                r'while\s*\(.*\)\s*{\s*\n.*while\s*\(.*\)\s*{'
            ],
            'simple_loops': [
                r'for\s*\(.*\)\s*{',
                r'while\s*\(.*\)\s*{',
                r'forEach\s*\('
            ],
            'recursion': [
                r'function\s+\w+\s*\(.*\)\s*{\s*\n.*\w+\s*\(.*\)',
                r'return\s+\w+\s*\(.*\)'
            ],
            'sorting': [
                r'\.sort\s*\(',
                r'sort\s*\('
            ]
        }
    
    def _get_java_patterns(self) -> Dict:
        """Patrones específicos para Java"""
        return {
            'nested_loops': [
                r'for\s*\(.*\)\s*{\s*\n.*for\s*\(.*\)\s*{',
                r'while\s*\(.*\)\s*{\s*\n.*while\s*\(.*\)\s*{'
            ],
            'simple_loops': [
                r'for\s*\(.*\)\s*{',
                r'while\s*\(.*\)\s*{',
                r'for\s*\(.*:\s*.*\)'
            ],
            'recursion': [
                r'public\s+.*\s+\w+\s*\(.*\)\s*{\s*\n.*\w+\s*\(.*\)',
                r'return\s+\w+\s*\(.*\)'
            ],
            'sorting': [
                r'\.sort\s*\(',
                r'Arrays\.sort',
                r'Collections\.sort'
            ]
        }
    
    def _get_cpp_patterns(self) -> Dict:
        """Patrones específicos para C++"""
        return {
            'nested_loops': [
                r'for\s*\(.*\)\s*{\s*\n.*for\s*\(.*\)\s*{',
                r'while\s*\(.*\)\s*{\s*\n.*while\s*\(.*\)\s*{'
            ],
            'simple_loops': [
                r'for\s*\(.*\)\s*{',
                r'while\s*\(.*\)\s*{'
            ],
            'recursion': [
                r'\w+\s+\w+\s*\(.*\)\s*{\s*\n.*\w+\s*\(.*\)',
                r'return\s+\w+\s*\(.*\)'
            ],
            'sorting': [
                r'sort\s*\(',
                r'std::sort'
            ]
        }
    
    def _detect_python_patterns(self, code: str) -> List[Dict]:
        """Detecta patrones específicos de Python"""
        patterns = []
        
        try:
            # Análisis AST para Python
            tree = ast.parse(code)
            patterns.extend(self._analyze_python_ast(tree))
        except:
            # Fallback a análisis de regex
            patterns.extend(self._analyze_regex_patterns(code, 'python'))
        
        return patterns
    
    def _analyze_python_ast(self, tree: ast.AST) -> List[Dict]:
        """Analiza el AST de Python para detectar patrones"""
        patterns = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                patterns.append({
                    'type': 'simple_loop',
                    'description': f'Bucle for en línea {node.lineno}',
                    'line': node.lineno
                })
            elif isinstance(node, ast.While):
                patterns.append({
                    'type': 'simple_loop',
                    'description': f'Bucle while en línea {node.lineno}',
                    'line': node.lineno
                })
            elif isinstance(node, ast.FunctionDef):
                # Buscar recursión
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                        if child.func.id == node.name:
                            patterns.append({
                                'type': 'recursion',
                                'description': f'Función recursiva {node.name} en línea {node.lineno}',
                                'line': node.lineno
                            })
                            break
        
        # Detectar bucles anidados
        nested_loops = self._detect_nested_loops_ast(tree)
        patterns.extend(nested_loops)
        
        return patterns
    
    def _detect_nested_loops_ast(self, tree: ast.AST) -> List[Dict]:
        """Detecta bucles anidados usando AST"""
        patterns = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                # Buscar bucles anidados dentro de este bucle
                for child in ast.walk(node):
                    if isinstance(child, (ast.For, ast.While)) and child != node:
                        patterns.append({
                            'type': 'nested_loop',
                            'description': f'Bucles anidados en líneas {node.lineno}-{child.lineno}',
                            'line': node.lineno
                        })
                        break
        
        return patterns
    
    def _detect_javascript_patterns(self, code: str) -> List[Dict]:
        """Detecta patrones específicos de JavaScript"""
        return self._analyze_regex_patterns(code, 'javascript')
    
    def _detect_java_patterns(self, code: str) -> List[Dict]:
        """Detecta patrones específicos de Java"""
        return self._analyze_regex_patterns(code, 'java')
    
    def _detect_cpp_patterns(self, code: str) -> List[Dict]:
        """Detecta patrones específicos de C++"""
        return self._analyze_regex_patterns(code, 'cpp')
    
    def _analyze_regex_patterns(self, code: str, language: str) -> List[Dict]:
        """Analiza patrones usando expresiones regulares"""
        patterns = []
        lang_patterns = self.patterns.get(language, {})
        
        for pattern_type, regex_list in lang_patterns.items():
            for regex in regex_list:
                matches = re.finditer(regex, code, re.MULTILINE | re.DOTALL)
                for match in matches:
                    patterns.append({
                        'type': pattern_type,
                        'description': f'Patrón {pattern_type} detectado',
                        'line': code[:match.start()].count('\n') + 1,
                        'match': match.group()
                    })
        
        return patterns
    
    def get_pattern_summary(self, patterns: List[Dict]) -> str:
        """Genera un resumen de los patrones detectados"""
        if not patterns:
            return "No se detectaron patrones específicos"
        
        summary = f"Se detectaron {len(patterns)} patrones:\n"
        
        pattern_counts = {}
        for pattern in patterns:
            pattern_type = pattern['type']
            pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
        
        for pattern_type, count in pattern_counts.items():
            summary += f"• {pattern_type}: {count} ocurrencias\n"
        
        return summary 