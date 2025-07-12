#!/usr/bin/env python3
"""
Generador de dataset para entrenamiento de la red neuronal
"""

from typing import List, Tuple
import random


class AlgorithmDatasetGenerator:
    """Genera ejemplos de algoritmos para entrenar la red neuronal"""
    
    def __init__(self):
        self.algorithms = self._create_algorithm_examples()
    
    def generate_training_dataset(self, samples_per_class: int = 50) -> List[Tuple[str, str]]:
        """Genera el dataset de entrenamiento con múltiples variaciones"""
        training_data = []
        
        for complexity, examples in self.algorithms.items():
            # Agregar ejemplos originales
            for code in examples:
                training_data.append((code, complexity))
            
            # Generar variaciones para aumentar el dataset
            for _ in range(samples_per_class - len(examples)):
                base_code = random.choice(examples)
                variation = self._create_variation(base_code)
                training_data.append((variation, complexity))
        
        # Mezclar el dataset
        random.shuffle(training_data)
        return training_data
    
    def _create_variation(self, code: str) -> str:
        """Crea variaciones del código para aumentar el dataset"""
        variations = [
            # Cambiar nombres de variables
            lambda c: c.replace('arr', random.choice(['data', 'list', 'nums', 'elements', 'array'])),
            lambda c: c.replace('target', random.choice(['item', 'element', 'search_value', 'key'])),
            lambda c: c.replace('n', random.choice(['size', 'length', 'count', 'len'])),
            
            # Cambiar nombres de funciones
            lambda c: c.replace('def ', 'def ' + random.choice(['algorithm_', 'sort_', 'search_', 'find_'])),
            
            # Agregar comentarios
            lambda c: c + f"\n# {random.choice(['Algorithm implementation', 'Sorting function', 'Search function', 'Complexity analysis'])}",
            
            # Cambiar estructura de control
            lambda c: c.replace('for i in range', 'for index in range'),
            lambda c: c.replace('for j in range', 'for j_index in range'),
            
            # Agregar espacios extra
            lambda c: c.replace(' = ', '  =  '),
            lambda c: c.replace('if ', 'if  '),
            
            # Cambiar operadores
            lambda c: c.replace(' > ', ' > '),
            lambda c: c.replace(' < ', ' < '),
            
            # Agregar variables extra
            lambda c: c.replace('def ', 'def ').replace(':', ':\n    # Initialize variables'),
        ]
        
        # Aplicar 1-3 variaciones aleatorias
        num_variations = random.randint(1, 3)
        for _ in range(num_variations):
            variation_func = random.choice(variations)
            code = variation_func(code)
        
        return code
    
    def _create_algorithm_examples(self) -> dict:
        """Crea ejemplos de algoritmos para cada clase de complejidad"""
        return {
            'O(1)': [
                # Acceso directo
                '''def get_first_element(arr):
    return arr[0]''',
                
                # Operación constante
                '''def add_numbers(a, b):
    return a + b''',
                
                # Asignación simple
                '''def assign_value():
    x = 42
    return x''',
                
                # Operación matemática
                '''def square_number(n):
    return n * n''',
                
                # Comparación
                '''def is_positive(n):
    return n > 0''',
                
                # Acceso a diccionario
                '''def get_value(dictionary, key):
    return dictionary.get(key, None)''',
                
                # Swap de elementos
                '''def swap_elements(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    return arr''',
                
                # Verificar si está vacío
                '''def is_empty(data):
    return len(data) == 0''',
                
                # Operación aritmética
                '''def simple_math(a, b, c):
    return a + b * c - 1''',
                
                # Acceso a propiedad
                '''def get_length(data):
    return len(data)'''
            ],
            
            'O(log n)': [
                # Búsqueda binaria
                '''def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1''',
                
                # Búsqueda en árbol
                '''def search_binary_tree(root, value):
    if root is None or root.value == value:
        return root
    if value < root.value:
        return search_binary_tree(root.left, value)
    return search_binary_tree(root.right, value)''',
                
                # División por 2
                '''def count_power_of_2(n):
    count = 0
    while n > 1:
        n = n // 2
        count += 1
    return count''',
                
                # Potencia eficiente
                '''def power_efficient(base, exponent):
    if exponent == 0:
        return 1
    if exponent % 2 == 0:
        return power_efficient(base * base, exponent // 2)
    return base * power_efficient(base * base, exponent // 2)''',
                
                # Búsqueda en array ordenado
                '''def find_in_sorted(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1''',
                
                # Logaritmo natural
                '''def natural_log(n):
    if n <= 1:
        return 0
    return 1 + natural_log(n / 2)''',
                
                # Búsqueda ternaria
                '''def ternary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3
        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2
        if target < arr[mid1]:
            right = mid1 - 1
        elif target > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1
    return -1'''
            ],
            
            'O(n)': [
                # Búsqueda lineal
                '''def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1''',
                
                # Recorrido de array
                '''def sum_array(arr):
    total = 0
    for num in arr:
        total += num
    return total''',
                
                # Filtrado
                '''def filter_even_numbers(arr):
    result = []
    for num in arr:
        if num % 2 == 0:
            result.append(num)
    return result''',
                
                # Encontrar máximo
                '''def find_max(arr):
    if not arr:
        return None
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val''',
                
                # Contar ocurrencias
                '''def count_occurrences(arr, target):
    count = 0
    for element in arr:
        if element == target:
            count += 1
    return count''',
                
                # Revertir array
                '''def reverse_array(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr''',
                
                # Encontrar mínimo
                '''def find_min(arr):
    if not arr:
        return None
    min_val = arr[0]
    for num in arr:
        if num < min_val:
            min_val = num
    return min_val''',
                
                # Promedio
                '''def calculate_average(arr):
    if not arr:
        return 0
    total = sum(arr)
    return total / len(arr)''',
                
                # Duplicados únicos
                '''def find_unique_duplicates(arr):
    seen = set()
    duplicates = set()
    for num in arr:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    return list(duplicates)''',
                
                # Rotar array
                '''def rotate_array(arr, k):
    n = len(arr)
    k = k % n
    return arr[k:] + arr[:k]'''
            ],
            
            'O(n log n)': [
                # Merge Sort
                '''def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result''',
                
                # Quick Sort
                '''def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)''',
                
                # Heap Sort
                '''def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr''',
                
                # Tim Sort (simplificado)
                '''def tim_sort(arr):
    # Usar sorted() que implementa TimSort en Python
    return sorted(arr)''',
                
                # Shell Sort
                '''def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr''',
                
                # Radix Sort
                '''def radix_sort(arr):
    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        
        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1
        
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        for i in range(n - 1, -1, -1):
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
        
        for i in range(n):
            arr[i] = output[i]
    
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr'''
            ],
            
            'O(n²)': [
                # Bubble Sort
                '''def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr''',
                
                # Selection Sort
                '''def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr''',
                
                # Insertion Sort
                '''def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr''',
                
                # Comparación de todos con todos
                '''def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates''',
                
                # Transponer matriz
                '''def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0 for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result''',
                
                # Suma de matrices
                '''def add_matrices(a, b):
    rows = len(a)
    cols = len(a[0])
    result = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result[i][j] = a[i][j] + b[i][j]
    return result''',
                
                # Búsqueda de subarray
                '''def find_subarray_sum(arr, target):
    for i in range(len(arr)):
        current_sum = 0
        for j in range(i, len(arr)):
            current_sum += arr[j]
            if current_sum == target:
                return arr[i:j+1]
    return None''',
                
                # Ordenamiento por conteo (simplificado)
                '''def counting_sort_simple(arr):
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    
    result = []
    for i in range(len(count)):
        result.extend([i] * count[i])
    return result'''
            ],
            
            'O(n³)': [
                # Multiplicación de matrices
                '''def matrix_multiply(a, b):
    n = len(a)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result''',
                
                # Tres bucles anidados
                '''def find_triplets(arr):
    triplets = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            for k in range(j + 1, len(arr)):
                if arr[i] + arr[j] + arr[k] == 0:
                    triplets.append([arr[i], arr[j], arr[k]])
    return triplets''',
                
                # Floyd-Warshall (simplificado)
                '''def floyd_warshall(graph):
    n = len(graph)
    dist = [row[:] for row in graph]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist''',
                
                # Producto de tres arrays
                '''def triple_product(a, b, c):
    result = 0
    for i in range(len(a)):
        for j in range(len(b)):
            for k in range(len(c)):
                result += a[i] * b[j] * c[k]
    return result''',
                
                # Búsqueda de patrones 3D
                '''def find_3d_pattern(matrix_3d):
    count = 0
    for i in range(len(matrix_3d)):
        for j in range(len(matrix_3d[0])):
            for k in range(len(matrix_3d[0][0])):
                if matrix_3d[i][j][k] == 1:
                    count += 1
    return count'''
            ],
            
            'O(2ⁿ)': [
                # Fibonacci recursivo
                '''def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)''',
                
                # Subconjuntos
                '''def generate_subsets(arr):
    if not arr:
        return [[]]
    
    first = arr[0]
    rest = arr[1:]
    subsets = generate_subsets(rest)
    
    result = []
    for subset in subsets:
        result.append(subset)
        result.append([first] + subset)
    
    return result''',
                
                # Torres de Hanoi
                '''def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    
    hanoi(n - 1, source, auxiliary, target)
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n - 1, auxiliary, target, source)''',
                
                # Suma de subconjuntos
                '''def subset_sum(arr, target):
    def backtrack(index, current_sum):
        if current_sum == target:
            return True
        if index >= len(arr) or current_sum > target:
            return False
        return backtrack(index + 1, current_sum + arr[index]) or backtrack(index + 1, current_sum)
    return backtrack(0, 0)''',
                
                # Generar combinaciones
                '''def generate_combinations(arr, r):
    if r == 0:
        return [[]]
    if len(arr) == 0:
        return []
    
    first = arr[0]
    rest = arr[1:]
    
    with_first = [[first] + combo for combo in generate_combinations(rest, r - 1)]
    without_first = generate_combinations(rest, r)
    
    return with_first + without_first''',
                
                # Backtracking simple
                '''def backtrack_simple(n):
    def solve(step):
        if step == n:
            return True
        for i in range(2):
            if solve(step + 1):
                return True
        return False
    return solve(0)''',
                
                # Recursión exponencial
                '''def exponential_recursion(n):
    if n <= 1:
        return 1
    return exponential_recursion(n - 1) + exponential_recursion(n - 1)'''
            ],
            
            'O(n!)': [
                # Permutaciones
                '''def generate_permutations(arr):
    if len(arr) <= 1:
        return [arr]
    
    permutations = []
    for i in range(len(arr)):
        current = arr[i]
        remaining = arr[:i] + arr[i + 1:]
        
        for perm in generate_permutations(remaining):
            permutations.append([current] + perm)
    
    return permutations''',
                
                # Factorial recursivo
                '''def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)''',
                
                # Backtracking simple
                '''def solve_n_queens(n):
    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
        return True
    
    def solve(board, row):
        if row == n:
            return True
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                if solve(board, row + 1):
                    return True
                board[row] = -1
        return False
    
    board = [-1] * n
    return solve(board, 0)''',
                
                # Viajante de comercio (simplificado)
                '''def traveling_salesman(graph):
    def calculate_cost(path):
        total = 0
        for i in range(len(path) - 1):
            total += graph[path[i]][path[i + 1]]
        total += graph[path[-1]][path[0]]
        return total
    
    def generate_all_paths(n):
        if n == 1:
            return [[0]]
        paths = []
        for perm in generate_permutations(list(range(1, n))):
            paths.append([0] + perm)
        return paths
    
    n = len(graph)
    all_paths = generate_all_paths(n)
    min_cost = float('inf')
    best_path = None
    
    for path in all_paths:
        cost = calculate_cost(path)
        if cost < min_cost:
            min_cost = cost
            best_path = path
    
    return best_path, min_cost''',
                
                # Generar todas las combinaciones
                '''def all_combinations(arr):
    if len(arr) == 0:
        return [[]]
    
    first = arr[0]
    rest = arr[1:]
    
    without_first = all_combinations(rest)
    with_first = [[first] + combo for combo in without_first]
    
    return without_first + with_first''',
                
                # Backtracking factorial
                '''def factorial_backtrack(n):
    def solve(step, used):
        if step == n:
            return True
        for i in range(n):
            if i not in used:
                used.add(i)
                if solve(step + 1, used):
                    return True
                used.remove(i)
        return False
    return solve(0, set())'''
            ]
        } 