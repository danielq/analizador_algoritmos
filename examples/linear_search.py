def linear_search(arr, target):
    """
    Algoritmo de búsqueda lineal
    Complejidad temporal: O(n)
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# Ejemplo de uso
if __name__ == "__main__":
    numbers = [10, 20, 30, 40, 50, 60, 70]
    target = 40
    result = linear_search(numbers, target)
    if result != -1:
        print(f"Elemento {target} encontrado en la posición {result}")
    else:
        print(f"Elemento {target} no encontrado") 