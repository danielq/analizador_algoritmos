# Analizador de Algoritmos - Calculadora de Notación Asintótica

## Descripción
Este programa analiza algoritmos escritos en diferentes lenguajes de programación y calcula automáticamente su notación asintótica (Big O, Big Omega, Big Theta).

## Características
- ✅ Análisis de algoritmos en múltiples lenguajes (Python, JavaScript, Java, C++)
- ✅ Interfaz gráfica intuitiva
- ✅ Interfaz de línea de comandos
- ✅ Detección automática de patrones de complejidad
- ✅ Visualización de resultados
- ✅ Soporte para algoritmos recursivos e iterativos

## Instalación
```bash
pip install -r requirements.txt
```

## Uso

### Interfaz Gráfica
```bash
python main.py --gui
```

### Línea de Comandos
```bash
python main.py --file algoritmo.py
python main.py --code "for i in range(n): print(i)"
```

## Ejemplos de Uso

### Algoritmo O(n)
```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

### Algoritmo O(n²)
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
```

## Estructura del Proyecto
```
analizador_algoritmos/
├── main.py                 # Punto de entrada principal
├── core/
│   ├── analyzer.py         # Analizador principal
│   ├── complexity.py       # Cálculo de complejidad
│   └── patterns.py         # Patrones de detección
├── gui/
│   ├── main_window.py      # Ventana principal
│   └── widgets.py          # Componentes de UI
├── cli/
│   └── commands.py         # Comandos CLI
└── utils/
    ├── parser.py           # Parsers de lenguajes
    └── visualizer.py       # Visualización de resultados
``` 