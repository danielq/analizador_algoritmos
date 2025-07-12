"""
Visualizador de resultados del análisis de algoritmos
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math


class ResultVisualizer:
    """Visualiza los resultados del análisis de algoritmos"""
    
    def __init__(self):
        self.complexity_colors = {
            'O(1)': '#2E8B57',      # Verde mar
            'O(log n)': '#4169E1',  # Azul real
            'O(n)': '#32CD32',      # Verde lima
            'O(n log n)': '#FF8C00', # Naranja oscuro
            'O(n²)': '#FF4500',     # Rojo naranja
            'O(n³)': '#DC143C',     # Carmesí
            'O(2ⁿ)': '#8B0000',     # Rojo oscuro
            'O(n!)': '#4B0082'      # Índigo
        }
    
    def create_complexity_chart(self, complexity_data: Dict) -> Figure:
        """Crea un gráfico de complejidad temporal"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico de barras de complejidades
        notations = list(self.complexity_colors.keys())
        colors = list(self.complexity_colors.values())
        
        # Simular datos de tiempo de ejecución para diferentes tamaños
        n_values = [10, 100, 1000, 10000]
        
        # Calcular tiempos para cada notación
        for i, notation in enumerate(notations):
            times = []
            for n in n_values:
                if notation == 'O(1)':
                    time = 1
                elif notation == 'O(log n)':
                    time = np.log2(n)
                elif notation == 'O(n)':
                    time = n
                elif notation == 'O(n log n)':
                    time = n * np.log2(n)
                elif notation == 'O(n²)':
                    time = n**2
                elif notation == 'O(n³)':
                    time = n**3
                elif notation == 'O(2ⁿ)':
                    time = 2**n if n <= 10 else 1000  # Limitar para visualización
                elif notation == 'O(n!)':
                    time = math.factorial(n) if n <= 8 else 1000  # Limitar para visualización
                else:
                    time = 1
                times.append(time)
            
            ax1.plot(n_values, times, color=colors[i], label=notation, linewidth=2, marker='o')
        
        ax1.set_xlabel('Tamaño de entrada (n)')
        ax1.set_ylabel('Tiempo de ejecución (relativo)')
        ax1.set_title('Comparación de Complejidades Temporales')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
        
        # Gráfico de pastel de distribución
        if 'terms' in complexity_data:
            terms = complexity_data['terms']
            if terms:
                term_types = [term['type'] for term in terms]
                term_counts = {}
                for term_type in term_types:
                    term_counts[term_type] = term_counts.get(term_type, 0) + 1
                
                labels = list(term_counts.keys())
                sizes = list(term_counts.values())
                colors_pie = [self.complexity_colors.get(f"O({label})", '#808080') for label in labels]
                
                ax2.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
                ax2.set_title('Distribución de Patrones Detectados')
        
        plt.tight_layout()
        return fig
    
    def create_tkinter_visualization(self, parent: tk.Widget, complexity_data: Dict) -> tk.Widget:
        """Crea una visualización en Tkinter"""
        # Frame para la visualización
        viz_frame = ttk.Frame(parent)
        
        # Crear gráfico
        fig = self.create_complexity_chart(complexity_data)
        
        # Integrar matplotlib con Tkinter
        canvas = FigureCanvasTkAgg(fig, viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return viz_frame
    
    def create_text_summary(self, result: Dict) -> str:
        """Crea un resumen textual de los resultados"""
        if not result.get('success'):
            return "❌ Error en el análisis"
        
        notation = result.get('notation', 'No determinado')
        explanation = result.get('explanation', '')
        
        summary = f"""
📊 RESUMEN DEL ANÁLISIS
{'='*50}

🎯 NOTACIÓN ASINTÓTICA: {notation}

📝 EXPLICACIÓN:
{explanation}

🔍 PATRONES DETECTADOS:
"""
        
        if result.get('patterns'):
            for i, pattern in enumerate(result['patterns'], 1):
                summary += f"{i}. {pattern['type']}: {pattern['description']}\n"
        else:
            summary += "No se detectaron patrones específicos\n"
        
        if result.get('complexity'):
            complexity = result['complexity']
            summary += f"\n🔬 DETALLES TÉCNICOS:\n"
            summary += f"• Término dominante: {complexity.get('dominant_term', 'O(1)')}\n"
            summary += f"• Complejidad total: {complexity.get('total_complexity', 'O(1)')}\n"
        
        return summary
    
    def create_complexity_guide(self) -> str:
        """Crea una guía de complejidades"""
        guide = """
📚 GUÍA DE COMPLEJIDADES TEMPORALES
{'='*50}

🟢 O(1) - Constante
   • Acceso directo a arrays
   • Operaciones aritméticas básicas
   • Ejemplo: arr[0], x + y

🔵 O(log n) - Logarítmica
   • Búsqueda binaria
   • Algoritmos de división y conquista
   • Ejemplo: binary_search()

🟢 O(n) - Lineal
   • Búsqueda lineal
   • Recorrido de arrays
   • Ejemplo: for i in range(n):

🟠 O(n log n) - Linealítmica
   • Merge Sort, Quick Sort, Heap Sort
   • Algoritmos de ordenamiento eficientes
   • Ejemplo: sorted(arr)

🟡 O(n²) - Cuadrática
   • Bubble Sort, Selection Sort
   • Bucles anidados
   • Ejemplo: for i in range(n): for j in range(n):

🔴 O(n³) - Cúbica
   • Multiplicación de matrices
   • Tres bucles anidados
   • Ejemplo: for i in range(n): for j in range(n): for k in range(n):

🟣 O(2ⁿ) - Exponencial
   • Fibonacci recursivo
   • Algoritmos de fuerza bruta
   • Ejemplo: def fib(n): return fib(n-1) + fib(n-2)

⚫ O(n!) - Factorial
   • Permutaciones
   • Algoritmos de backtracking
   • Ejemplo: generar todas las permutaciones
"""
        return guide
    
    def create_performance_comparison(self, algorithms: List[Dict]) -> Figure:
        """Crea una comparación de rendimiento entre algoritmos"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        n_values = np.logspace(1, 4, 100)  # 10 a 10000
        
        for algorithm in algorithms:
            name = algorithm.get('name', 'Algoritmo')
            notation = algorithm.get('notation', 'O(n)')
            
            # Calcular tiempos
            times = []
            for n in n_values:
                if notation == 'O(1)':
                    time = 1
                elif notation == 'O(log n)':
                    time = np.log2(n)
                elif notation == 'O(n)':
                    time = n
                elif notation == 'O(n log n)':
                    time = n * np.log2(n)
                elif notation == 'O(n²)':
                    time = n**2
                elif notation == 'O(n³)':
                    time = n**3
                elif notation == 'O(2ⁿ)':
                    time = 2**n if n <= 10 else 1000
                elif notation == 'O(n!)':
                    time = math.factorial(n) if n <= 8 else 1000
                else:
                    time = n
                times.append(time)
            
            color = self.complexity_colors.get(notation, '#808080')
            ax.plot(n_values, times, label=f"{name} ({notation})", color=color, linewidth=2)
        
        ax.set_xlabel('Tamaño de entrada (n)')
        ax.set_ylabel('Tiempo de ejecución (relativo)')
        ax.set_title('Comparación de Rendimiento de Algoritmos')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')
        ax.set_xscale('log')
        
        plt.tight_layout()
        return fig 