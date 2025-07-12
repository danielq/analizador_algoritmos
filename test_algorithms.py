#!/usr/bin/env python3
"""
Archivo de prueba con diferentes algoritmos para testear el analizador
"""

def bubble_sort(arr):
    """Bubble Sort - O(n²)"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def binary_search(arr, target):
    """Binary Search - O(log n)"""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def linear_search(arr, target):
    """Linear Search - O(n)"""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def fibonacci_recursive(n):
    """Fibonacci Recursive - O(2ⁿ)"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def factorial(n):
    """Factorial - O(n)"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def matrix_multiply(a, b):
    """Matrix Multiplication - O(n³)"""
    n = len(a)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result

def get_first_element(arr):
    """Get First Element - O(1)"""
    return arr[0] if arr else None

# Ejemplo de uso
if __name__ == "__main__":
    # Test bubble sort
    numbers = [64, 34, 25, 12, 22, 11, 90]
    sorted_numbers = bubble_sort(numbers.copy())
    print(f"Bubble Sort: {sorted_numbers}")
    
    # Test binary search
    sorted_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = binary_search(sorted_arr, 7)
    print(f"Binary Search for 7: {result}")
    
    # Test linear search
    result = linear_search([1, 5, 3, 7, 9], 3)
    print(f"Linear Search for 3: {result}")
    
    # Test factorial
    fact = factorial(5)
    print(f"Factorial of 5: {fact}") 