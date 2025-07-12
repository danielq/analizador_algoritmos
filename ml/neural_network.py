"""
Red Neuronal para Clasificación de Complejidad de Algoritmos
"""

import numpy as np
import tensorflow as tf
import keras
from keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import json
from typing import Dict, List, Tuple, Optional
import re


class AlgorithmClassifier:
    """Clasificador de algoritmos usando red neuronal"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.feature_names = [
            'num_loops', 'num_nested_loops', 'max_nesting_level',
            'num_recursive_calls', 'num_conditionals', 'num_assignments',
            'num_function_calls', 'code_length', 'num_variables',
            'has_sorting', 'has_search', 'has_math_operations',
            'complexity_keywords', 'loop_patterns', 'recursion_patterns'
        ]
        
        if model_path:
            self.load_model(model_path)
    
    def extract_features(self, code: str, language: str = 'python') -> np.ndarray:
        """Extrae características del código fuente"""
        features = []
        
        # Características básicas
        features.append(self._count_loops(code))
        features.append(self._count_nested_loops(code))
        features.append(self._get_max_nesting_level(code))
        features.append(self._count_recursive_calls(code))
        features.append(self._count_conditionals(code))
        features.append(self._count_assignments(code))
        features.append(self._count_function_calls(code))
        features.append(len(code))
        features.append(self._count_variables(code))
        
        # Características específicas
        features.append(1 if self._has_sorting(code) else 0)
        features.append(1 if self._has_search(code) else 0)
        features.append(1 if self._has_math_operations(code) else 0)
        features.append(self._count_complexity_keywords(code))
        features.append(self._analyze_loop_patterns(code))
        features.append(self._analyze_recursion_patterns(code))
        
        return np.array(features, dtype=np.float32)
    
    def _count_loops(self, code: str) -> int:
        """Cuenta el número de bucles"""
        patterns = [
            r'\bfor\s+.*\s+in\s+',
            r'\bwhile\s+.*:',
            r'\bfor\s*\(.*\)',
            r'\bwhile\s*\(.*\)'
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, code, re.IGNORECASE))
        return count
    
    def _count_nested_loops(self, code: str) -> int:
        """Cuenta bucles anidados"""
        lines = code.split('\n')
        nested_count = 0
        current_indent = 0
        
        for line in lines:
            if re.search(r'\bfor\s+|while\s+', line):
                indent = len(line) - len(line.lstrip())
                if indent > current_indent:
                    nested_count += 1
                current_indent = indent
            else:
                indent = len(line) - len(line.lstrip())
                current_indent = indent
        
        return nested_count
    
    def _get_max_nesting_level(self, code: str) -> int:
        """Obtiene el nivel máximo de anidamiento"""
        lines = code.split('\n')
        max_level = 0
        current_level = 0
        
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                level = indent // 4  # Asumiendo 4 espacios por nivel
                max_level = max(max_level, level)
        
        return max_level
    
    def _count_recursive_calls(self, code: str) -> int:
        """Cuenta llamadas recursivas"""
        # Buscar patrones de recursión
        patterns = [
            r'\b\w+\s*\([^)]*\)',  # Llamadas de función
        ]
        
        # Extraer nombres de funciones definidas
        func_pattern = r'def\s+(\w+)\s*\('
        defined_functions = re.findall(func_pattern, code)
        
        recursive_calls = 0
        for func_name in defined_functions:
            call_pattern = rf'\b{func_name}\s*\('
            recursive_calls += len(re.findall(call_pattern, code))
        
        return recursive_calls
    
    def _count_conditionals(self, code: str) -> int:
        """Cuenta estructuras condicionales"""
        patterns = [
            r'\bif\s+',
            r'\belif\s+',
            r'\belse\s*:',
            r'\bswitch\s*\(',
            r'\bcase\s+'
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, code, re.IGNORECASE))
        return count
    
    def _count_assignments(self, code: str) -> int:
        """Cuenta asignaciones"""
        patterns = [
            r'\w+\s*=',
            r'\w+\s*\+=',
            r'\w+\s*-=',
            r'\w+\s*\*=',
            r'\w+\s*/='
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, code))
        return count
    
    def _count_function_calls(self, code: str) -> int:
        """Cuenta llamadas de función"""
        pattern = r'\w+\s*\('
        return len(re.findall(pattern, code))
    
    def _count_variables(self, code: str) -> int:
        """Cuenta variables declaradas"""
        patterns = [
            r'\bvar\s+\w+',
            r'\blet\s+\w+',
            r'\bconst\s+\w+',
            r'\bint\s+\w+',
            r'\bfloat\s+\w+',
            r'\bstring\s+\w+',
            r'\bdef\s+\w+\s*\([^)]*\):'
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, code, re.IGNORECASE))
        return count
    
    def _has_sorting(self, code: str) -> bool:
        """Verifica si el código contiene algoritmos de ordenamiento"""
        sorting_keywords = [
            'sort', 'sorted', 'bubble', 'quick', 'merge', 'heap',
            'selection', 'insertion', 'radix', 'counting'
        ]
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in sorting_keywords)
    
    def _has_search(self, code: str) -> bool:
        """Verifica si el código contiene algoritmos de búsqueda"""
        search_keywords = [
            'search', 'find', 'binary', 'linear', 'sequential'
        ]
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in search_keywords)
    
    def _has_math_operations(self, code: str) -> bool:
        """Verifica si el código contiene operaciones matemáticas"""
        math_patterns = [
            r'\+', r'-', r'\*', r'/', r'%', r'\*\*',
            r'math\.', r'np\.', r'sqrt', r'log', r'exp'
        ]
        return any(re.search(pattern, code) for pattern in math_patterns)
    
    def _count_complexity_keywords(self, code: str) -> int:
        """Cuenta palabras clave relacionadas con complejidad"""
        complexity_keywords = [
            'o(n)', 'o(n²)', 'o(n³)', 'o(log n)', 'o(n log n)',
            'o(2ⁿ)', 'o(n!)', 'complexity', 'time', 'space'
        ]
        code_lower = code.lower()
        count = 0
        for keyword in complexity_keywords:
            count += code_lower.count(keyword)
        return count
    
    def _analyze_loop_patterns(self, code: str) -> float:
        """Analiza patrones de bucles"""
        # Puntuación basada en patrones de bucles
        score = 0.0
        
        # Bucles simples
        if re.search(r'for\s+.*\s+in\s+range', code):
            score += 1.0
        
        # Bucles anidados
        nested_pattern = r'for\s+.*\s+in\s+.*:\s*\n.*for\s+.*\s+in\s+'
        if re.search(nested_pattern, code, re.MULTILINE):
            score += 2.0
        
        # Bucles con condiciones
        if re.search(r'for\s+.*\s+in\s+.*:\s*\n.*if\s+', code, re.MULTILINE):
            score += 0.5
        
        return score
    
    def _analyze_recursion_patterns(self, code: str) -> float:
        """Analiza patrones de recursión"""
        score = 0.0
        
        # Función recursiva
        func_pattern = r'def\s+(\w+)\s*\([^)]*\):'
        functions = re.findall(func_pattern, code)
        
        for func_name in functions:
            # Buscar llamada recursiva
            call_pattern = rf'\b{func_name}\s*\('
            if len(re.findall(call_pattern, code)) > 1:  # Más de una llamada
                score += 3.0
        
        # Patrones específicos de recursión
        if 'fibonacci' in code.lower():
            score += 1.0
        if 'factorial' in code.lower():
            score += 1.0
        
        return score
    
    def build_model(self, num_classes: int) -> keras.Model:
        """Construye el modelo de red neuronal"""
        model = keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(len(self.feature_names),)),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, training_data: List[Tuple[str, str]], epochs: int = 100, batch_size: int = 32):
        """Entrena el modelo con datos de entrenamiento"""
        # Preparar datos
        X = []
        y = []
        
        for code, complexity in training_data:
            features = self.extract_features(code)
            X.append(features)
            y.append(complexity)
        
        X = np.array(X)
        y = np.array(y)
        
        # Codificar etiquetas
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42
        )
        
        # Construir y entrenar modelo
        classes = self.label_encoder.classes_
        num_classes = len(classes) if classes is not None else 0
        self.model = self.build_model(num_classes)
        
        # Callbacks
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=10, restore_best_weights=True
        )
        
        # Entrenar
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            callbacks=[early_stopping],
            verbose="1"
        )
        
        # Evaluar
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose="0")
        print(f"Precisión en test: {test_accuracy:.4f}")
        
        return history
    
    def predict(self, code: str) -> Tuple[str, float]:
        """Predice la complejidad de un algoritmo"""
        if self.model is None:
            raise ValueError("Modelo no entrenado. Llama a train() primero.")
        
        features = self.extract_features(code)
        features = features.reshape(1, -1)
        
        prediction = self.model.predict(features, verbose="0")
        predicted_class = np.argmax(prediction[0])
        confidence = np.max(prediction[0])
        
        complexity = self.label_encoder.inverse_transform([predicted_class])[0]
        
        return complexity, confidence
    
    def save_model(self, model_path: str):
        """Guarda el modelo entrenado"""
        if self.model is None:
            raise ValueError("No hay modelo para guardar")
        
        # Guardar modelo
        self.model.save(f"{model_path}_model.h5")
        
        # Guardar encoder y metadatos
        classes = self.label_encoder.classes_
        metadata = {
            'label_encoder': list(classes) if classes is not None else [],
            'feature_names': self.feature_names
        }
        
        with open(f"{model_path}_metadata.json", 'w') as f:
            json.dump(metadata, f)
    
    def load_model(self, model_path: str):
        """Carga un modelo entrenado"""
        # Cargar modelo
        self.model = keras.models.load_model(f"{model_path}_model.h5")
        
        # Cargar metadatos
        with open(f"{model_path}_metadata.json", 'r') as f:
            metadata = json.load(f)
        
        self.label_encoder.classes_ = np.array(metadata['label_encoder'])
        self.feature_names = metadata['feature_names']
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Obtiene la importancia de las características"""
        if self.model is None:
            raise ValueError("Modelo no entrenado")
        
        # Usar los pesos de la primera capa como medida de importancia
        weights = self.model.layers[0].get_weights()[0]
        importance = np.mean(np.abs(weights), axis=1)
        
        return dict(zip(self.feature_names, importance)) 