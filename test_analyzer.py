#!/usr/bin/env python3
"""
Script de prueba para el analizador de algoritmos
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from core.analyzer import AlgorithmAnalyzer


def test_analyzer():
    """Prueba el analizador con diferentes algoritmos"""
    analyzer = AlgorithmAnalyzer()
    
    print("🧪 PRUEBAS DEL ANALIZADOR DE ALGORITMOS")
    print("=" * 50)
    
    # Test 1: Bubble Sort (O(n²))
    print("\n📝 Test 1: Bubble Sort")
    bubble_sort_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"""
    result = analyzer.analyze_code(bubble_sort_code, 'python')
    print(f"Resultado: {result.get('notation', 'No determinado')}")
    print(f"Éxito: {result.get('success', False)}")
    
    # Test 2: Linear Search (O(n))
    print("\n📝 Test 2: Linear Search")
    linear_search_code = """
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
"""
    result = analyzer.analyze_code(linear_search_code, 'python')
    print(f"Resultado: {result.get('notation', 'No determinado')}")
    print(f"Éxito: {result.get('success', False)}")
    
    # Test 3: Fibonacci Recursive (O(2ⁿ))
    print("\n📝 Test 3: Fibonacci Recursive")
    fibonacci_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    result = analyzer.analyze_code(fibonacci_code, 'python')
    print(f"Resultado: {result.get('notation', 'No determinado')}")
    print(f"Éxito: {result.get('success', False)}")
    
    # Test 4: Constant Time (O(1))
    print("\n📝 Test 4: Constant Time")
    constant_code = """
def get_first_element(arr):
    return arr[0] if arr else None
"""
    result = analyzer.analyze_code(constant_code, 'python')
    print(f"Resultado: {result.get('notation', 'No determinado')}")
    print(f"Éxito: {result.get('success', False)}")
    
    # Test 5: Archivo de ejemplo
    print("\n📝 Test 5: Archivo de ejemplo")
    try:
        result = analyzer.analyze_file('examples/bubble_sort.py', 'python')
        print(f"Resultado: {result.get('notation', 'No determinado')}")
        print(f"Éxito: {result.get('success', False)}")
    except Exception as e:
        print(f"Error al analizar archivo: {e}")
    
    print("\n✅ Pruebas completadas")


if __name__ == "__main__":
    test_analyzer() 