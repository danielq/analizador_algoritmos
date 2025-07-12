# 🧠 Machine Learning en el Analizador de Algoritmos

## Descripción
Este módulo integra una red neuronal que aprende a clasificar algoritmos basándose en características extraídas del código fuente, mejorando significativamente la precisión del análisis de complejidad temporal.

## Características

### 🔧 Red Neuronal
- **Arquitectura**: Red neuronal densa con 3 capas ocultas
- **Entrada**: 15 características extraídas del código
- **Salida**: Clasificación en 8 categorías de complejidad
- **Optimización**: Adam optimizer con early stopping

### 📊 Características Extraídas
1. `num_loops` - Número de bucles
2. `num_nested_loops` - Bucles anidados
3. `max_nesting_level` - Nivel máximo de anidamiento
4. `num_recursive_calls` - Llamadas recursivas
5. `num_conditionals` - Estructuras condicionales
6. `num_assignments` - Asignaciones
7. `num_function_calls` - Llamadas de función
8. `code_length` - Longitud del código
9. `num_variables` - Variables declaradas
10. `has_sorting` - Algoritmos de ordenamiento
11. `has_search` - Algoritmos de búsqueda
12. `has_math_operations` - Operaciones matemáticas
13. `complexity_keywords` - Palabras clave de complejidad
14. `loop_patterns` - Patrones de bucles
15. `recursion_patterns` - Patrones de recursión

## Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Verificar instalación
```bash
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
python -c "import sklearn; print('Scikit-learn:', sklearn.__version__)"
```

## Uso

### 1. Entrenar el Modelo

#### Entrenamiento básico:
```bash
python train_model.py
```

#### Entrenamiento personalizado:
```bash
python train_model.py --samples 200 --epochs 150 --batch-size 64 --test
```

#### Parámetros disponibles:
- `--samples`: Muestras por clase (default: 100)
- `--epochs`: Número de épocas (default: 100)
- `--batch-size`: Tamaño del batch (default: 32)
- `--model-path`: Ruta para guardar el modelo
- `--test`: Ejecutar pruebas después del entrenamiento

### 2. Usar el Modelo en el Analizador

#### En el código:
```python
from core.analyzer import AlgorithmAnalyzer

# Con red neuronal
analyzer = AlgorithmAnalyzer(use_neural_network=True, model_path="models/algorithm_classifier")

# Sin red neuronal
analyzer = AlgorithmAnalyzer(use_neural_network=False)

# Habilitar/deshabilitar dinámicamente
analyzer.enable_neural_network("models/algorithm_classifier")
analyzer.disable_neural_network()
```

#### En la línea de comandos:
```bash
# Usar con modelo entrenado
python main.py --file algoritmo.py --neural-model models/algorithm_classifier

# Usar solo análisis tradicional
python main.py --file algoritmo.py --no-neural
```

### 3. Generar Dataset Personalizado

```python
from ml.dataset_generator import DatasetGenerator

generator = DatasetGenerator()
dataset = generator.generate_training_dataset(samples_per_class=150)
stats = generator.get_dataset_statistics(dataset)
print(stats)
```

## Estructura del Proyecto ML

```
ml/
├── __init__.py              # Inicialización del módulo
├── neural_network.py        # Clasificador de red neuronal
└── dataset_generator.py     # Generador de datasets

models/                      # Modelos entrenados
├── algorithm_classifier_model.h5
├── algorithm_classifier_metadata.json
└── algorithm_classifier_metrics.json

train_model.py               # Script de entrenamiento
```

## Métricas de Rendimiento

### Dataset de Entrenamiento
- **Total de muestras**: 800 (100 por clase)
- **Distribución balanceada**: 8 clases de complejidad
- **Longitud promedio**: ~200 caracteres por algoritmo

### Precisión Esperada
- **Precisión en entrenamiento**: >95%
- **Precisión en validación**: >90%
- **Confianza promedio**: >85%

### Clases de Complejidad
1. **O(1)** - Constante
2. **O(log n)** - Logarítmica
3. **O(n)** - Lineal
4. **O(n log n)** - Linealítmica
5. **O(n²)** - Cuadrática
6. **O(n³)** - Cúbica
7. **O(2ⁿ)** - Exponencial
8. **O(n!)** - Factorial

## Ventajas del Machine Learning

### 🎯 Precisión Mejorada
- Aprende patrones complejos no capturados por reglas
- Mejora con más datos de entrenamiento
- Adaptable a diferentes estilos de código

### 🔄 Aprendizaje Continuo
- Se puede reentrenar con nuevos ejemplos
- Mejora la precisión con el tiempo
- Adaptable a nuevos patrones

### 🤖 Automatización
- Reduce la necesidad de reglas manuales
- Detecta patrones sutiles
- Escalable a nuevos lenguajes

## Limitaciones

### 📝 Dependencia de Datos
- Requiere dataset de entrenamiento
- Calidad depende de ejemplos de entrenamiento
- Necesita reentrenamiento para nuevos patrones

### ⚡ Rendimiento
- Más lento que análisis tradicional
- Requiere más recursos computacionales
- Dependencia de TensorFlow

### 🔍 Interpretabilidad
- Menos interpretable que reglas tradicionales
- Difícil explicar decisiones específicas
- Requiere análisis de importancia de características

## Mejoras Futuras

### 🚀 Características Adicionales
- Análisis semántico del código
- Detección de optimizaciones
- Análisis de memoria (complejidad espacial)

### 🧠 Arquitecturas Avanzadas
- Redes neuronales recurrentes (RNN)
- Transformers para análisis de código
- Modelos pre-entrenados

### 📊 Datasets Mejorados
- Datasets de código real
- Múltiples lenguajes de programación
- Anotaciones de expertos

## Troubleshooting

### Error: "No module named 'tensorflow'"
```bash
pip install tensorflow
```

### Error: "CUDA not available"
```bash
pip install tensorflow-cpu  # Para CPU only
```

### Error: "Model not found"
```bash
python train_model.py  # Entrenar modelo primero
```

### Baja precisión
- Aumentar `--samples` (más datos)
- Aumentar `--epochs` (más entrenamiento)
- Verificar calidad del dataset

## Contribuir

1. **Agregar nuevos algoritmos** al `DatasetGenerator`
2. **Mejorar características** en `AlgorithmClassifier`
3. **Optimizar arquitectura** de la red neuronal
4. **Crear datasets** de código real
5. **Documentar** nuevos patrones de complejidad 