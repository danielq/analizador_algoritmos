"""
Ventana principal de la interfaz gráfica del analizador de algoritmos
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from typing import Optional

from core.analyzer import AlgorithmAnalyzer


class AlgorithmAnalyzerGUI:
    """Interfaz gráfica principal del analizador de algoritmos"""
    
    def __init__(self):
        self.analyzer = AlgorithmAnalyzer()
        self.root = tk.Tk()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.root.title("Analizador de Algoritmos - Notación Asintótica")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Analizador de Algoritmos", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selector de lenguaje
        ttk.Label(main_frame, text="Lenguaje:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.language_var = tk.StringVar(value='python')
        language_combo = ttk.Combobox(main_frame, textvariable=self.language_var,
                                     values=['python', 'javascript', 'java', 'cpp'],
                                     state='readonly', width=15)
        language_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 10))
        
        # Botón cargar archivo
        load_btn = ttk.Button(main_frame, text="Cargar Archivo", command=self.load_file)
        load_btn.grid(row=1, column=2, padx=(0, 10))
        
        # Área de código
        ttk.Label(main_frame, text="Código del algoritmo:").grid(row=2, column=0, sticky="wn", pady=(20, 5))
        
        self.code_text = scrolledtext.ScrolledText(main_frame, width=80, height=20,
                                                  font=('Consolas', 10))
        self.code_text.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(0, 20))
        
        # Botón analizar
        analyze_btn = ttk.Button(main_frame, text="Analizar Algoritmo", 
                                command=self.analyze_algorithm, style='Accent.TButton')
        analyze_btn.grid(row=4, column=0, columnspan=3, pady=(0, 20))
        
        # Área de resultados
        ttk.Label(main_frame, text="Resultados:").grid(row=5, column=0, sticky="wn", pady=(0, 5))
        
        self.result_text = scrolledtext.ScrolledText(main_frame, width=80, height=10,
                                                    font=('Arial', 10), state='disabled')
        self.result_text.grid(row=6, column=0, columnspan=3, sticky="nsew")
        
        # Código de ejemplo
        self.insert_example_code()
        
    def load_file(self):
        """Carga un archivo de código"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de código",
            filetypes=[
                ("Python", "*.py"),
                ("JavaScript", "*.js"),
                ("Java", "*.java"),
                ("C++", "*.cpp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    self.code_text.delete(1.0, tk.END)
                    self.code_text.insert(1.0, code)
                    
                # Detectar lenguaje por extensión
                ext = file_path.split('.')[-1].lower()
                lang_map = {'py': 'python', 'js': 'javascript', 'java': 'java', 'cpp': 'cpp'}
                if ext in lang_map:
                    self.language_var.set(lang_map[ext])
                    
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
    
    def analyze_algorithm(self):
        """Analiza el algoritmo ingresado"""
        code = self.code_text.get(1.0, tk.END).strip()
        language = self.language_var.get()
        
        if not code:
            messagebox.showwarning("Advertencia", "Por favor ingrese código para analizar")
            return
            
        try:
            # Mostrar indicador de progreso
            self.root.config(cursor="wait")
            self.root.update()
            
            # Analizar código
            result = self.analyzer.analyze_code(code, language)
            
            # Mostrar resultados
            self.display_results(result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar el código: {e}")
        finally:
            self.root.config(cursor="")
    
    def display_results(self, result: dict):
        """Muestra los resultados del análisis"""
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        
        if result.get('success'):
            notation = result.get('notation', 'No determinado')
            explanation = result.get('explanation', '')
            
            output = f"✅ ANÁLISIS COMPLETADO\n\n"
            output += f"📊 NOTACIÓN ASINTÓTICA: {notation}\n\n"
            output += f"📝 EXPLICACIÓN:\n{explanation}\n\n"
            
            if result.get('patterns'):
                output += "🔍 PATRONES DETECTADOS:\n"
                for pattern in result['patterns']:
                    output += f"• {pattern['type']}: {pattern['description']}\n"
        else:
            output = f"❌ ERROR EN EL ANÁLISIS\n\n"
            output += f"Error: {result.get('error', 'Error desconocido')}"
        
        self.result_text.insert(1.0, output)
        self.result_text.config(state='disabled')
    
    def insert_example_code(self):
        """Inserta código de ejemplo"""
        example_code = '''def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Ejemplo de uso
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)'''
        
        self.code_text.insert(1.0, example_code)
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop() 