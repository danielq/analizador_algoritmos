def fibonacci_recursive(n):
    """
    Algoritmo de Fibonacci recursivo
    Complejidad temporal: O(2ⁿ)
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

# Ejemplo de uso
if __name__ == "__main__":
    n = 10
    result = fibonacci_recursive(n)
    print(f"Fibonacci({n}) = {result}")
    
    # Mostrar primeros 10 números de Fibonacci
    print("Primeros 10 números de Fibonacci:")
    for i in range(10):
        print(f"F({i}) = {fibonacci_recursive(i)}") 