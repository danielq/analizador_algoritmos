def bubble_sort(arr):
    """
    Algoritmo de ordenamiento Bubble Sort
    Complejidad temporal: O(n²)
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Ejemplo de uso
if __name__ == "__main__":
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print("Array original:", numbers)
    sorted_numbers = bubble_sort(numbers)
    print("Array ordenado:", sorted_numbers) 