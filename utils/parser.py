"""
Parser de código para diferentes lenguajes de programación
"""

import ast
import re
from typing import Dict, Any, Optional


class CodeParser:
    """Parser para diferentes lenguajes de programación"""
    
    def __init__(self):
        self.supported_languages = ['python', 'javascript', 'java', 'cpp']
    
    def parse(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """
        Parsea código según el lenguaje especificado
        
        Args:
            code: Código fuente a parsear
            language: Lenguaje de programación
            
        Returns:
            Diccionario con información parseada
        """
        if language not in self.supported_languages:
            raise ValueError(f"Lenguaje no soportado: {language}")
        
        if language == 'python':
            return self._parse_python(code)
        elif language == 'javascript':
            return self._parse_javascript(code)
        elif language == 'java':
            return self._parse_java(code)
        elif language == 'cpp':
            return self._parse_cpp(code)
        
        return {'raw_code': code, 'language': language}
    
    def _parse_python(self, code: str) -> Dict[str, Any]:
        """Parsea código Python usando AST"""
        try:
            tree = ast.parse(code)
            
            # Extraer información básica
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args]
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'line': node.lineno
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}")
            
            return {
                'language': 'python',
                'ast_tree': tree,
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'raw_code': code,
                'parse_success': True
            }
            
        except SyntaxError as e:
            return {
                'language': 'python',
                'raw_code': code,
                'parse_success': False,
                'error': str(e)
            }
    
    def _parse_javascript(self, code: str) -> Dict[str, Any]:
        """Parsea código JavaScript usando regex"""
        functions = []
        classes = []
        imports = []
        
        # Detectar funciones
        function_pattern = r'function\s+(\w+)\s*\([^)]*\)\s*{'
        for match in re.finditer(function_pattern, code):
            functions.append({
                'name': match.group(1),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Detectar arrow functions
        arrow_pattern = r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>'
        for match in re.finditer(arrow_pattern, code):
            functions.append({
                'name': match.group(1),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Detectar clases
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, code):
            classes.append({
                'name': match.group(1),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Detectar imports
        import_patterns = [
            r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        ]
        
        for pattern in import_patterns:
            for match in re.finditer(pattern, code):
                imports.append(match.group(1))
        
        return {
            'language': 'javascript',
            'functions': functions,
            'classes': classes,
            'imports': imports,
            'raw_code': code,
            'parse_success': True
        }
    
    def _parse_java(self, code: str) -> Dict[str, Any]:
        """Parsea código Java usando regex"""
        functions = []
        classes = []
        imports = []
        
        # Detectar métodos
        method_pattern = r'(public|private|protected)?\s*(static)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*{'
        for match in re.finditer(method_pattern, code):
            functions.append({
                'name': match.group(3),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Detectar clases
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, code):
            classes.append({
                'name': match.group(1),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Detectar imports
        import_pattern = r'import\s+([^;]+);'
        for match in re.finditer(import_pattern, code):
            imports.append(match.group(1).strip())
        
        return {
            'language': 'java',
            'functions': functions,
            'classes': classes,
            'imports': imports,
            'raw_code': code,
            'parse_success': True
        }
    
    def _parse_cpp(self, code: str) -> Dict[str, Any]:
        """Parsea código C++ usando regex"""
        functions = []
        classes = []
        imports = []
        
        # Detectar funciones
        function_pattern = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{'
        for match in re.finditer(function_pattern, code):
            functions.append({
                'name': match.group(2),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Detectar clases
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, code):
            classes.append({
                'name': match.group(1),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Detectar includes
        include_pattern = r'#include\s*[<"]([^>"]+)[>"]'
        for match in re.finditer(include_pattern, code):
            imports.append(match.group(1))
        
        return {
            'language': 'cpp',
            'functions': functions,
            'classes': classes,
            'imports': imports,
            'raw_code': code,
            'parse_success': True
        }
    
    def get_language_info(self, language: str) -> Dict[str, str]:
        """Retorna información sobre el lenguaje"""
        info = {
            'python': {
                'name': 'Python',
                'extension': '.py',
                'description': 'Lenguaje de programación interpretado y de alto nivel'
            },
            'javascript': {
                'name': 'JavaScript',
                'extension': '.js',
                'description': 'Lenguaje de programación interpretado para desarrollo web'
            },
            'java': {
                'name': 'Java',
                'extension': '.java',
                'description': 'Lenguaje de programación orientado a objetos compilado'
            },
            'cpp': {
                'name': 'C++',
                'extension': '.cpp',
                'description': 'Lenguaje de programación compilado de propósito general'
            }
        }
        
        return info.get(language, {})
    
    def validate_syntax(self, code: str, language: str) -> Dict[str, Any]:
        """Valida la sintaxis del código"""
        try:
            if language == 'python':
                ast.parse(code)
                return {'valid': True, 'language': language}
            else:
                # Para otros lenguajes, asumimos que es válido si se puede parsear
                self.parse(code, language)
                return {'valid': True, 'language': language}
        except Exception as e:
            return {
                'valid': False,
                'language': language,
                'error': str(e)
            } 