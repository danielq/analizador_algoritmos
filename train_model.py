#!/usr/bin/env python3
"""
Script para entrenar la red neuronal del analizador de algoritmos
"""

import sys
import os
from pathlib import Path
import argparse
import json

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from ml.neural_network import AlgorithmClassifier
from ml.dataset_generator import AlgorithmDatasetGenerator


def train_model(samples_per_class: int = 100, epochs: int = 100, 
                batch_size: int = 32, model_path: str = "models/algorithm_classifier"):
    """Entrena el modelo de clasificación de algoritmos"""
    
    print("🧠 ENTRENAMIENTO DE RED NEURONAL")
    print("=" * 50)
    
    # Crear directorio para modelos si no existe
    os.makedirs("models", exist_ok=True)
    
    # Generar dataset
    print("📊 Generando dataset de entrenamiento...")
    generator = AlgorithmDatasetGenerator()
    dataset = generator.generate_training_dataset(samples_per_class=100)
    
    # Mostrar estadísticas del dataset
    print(f"Total de muestras: {len(dataset)}")
    print("Dataset generado exitosamente")
    
    # Crear y entrenar el clasificador
    print("\n🔧 Creando clasificador...")
    classifier = AlgorithmClassifier()
    
    print(f"\n🚀 Iniciando entrenamiento...")
    print(f"Épocas: {epochs}")
    print(f"Batch size: {batch_size}")
    print(f"Muestras por clase: {samples_per_class}")
    
    # Entrenar el modelo
    history = classifier.train(dataset, epochs=epochs, batch_size=batch_size)
    
    # Guardar el modelo
    print(f"\n💾 Guardando modelo en {model_path}...")
    classifier.save_model(model_path)
    
    # Mostrar importancia de características
    print("\n📈 Importancia de características:")
    feature_importance = classifier.get_feature_importance()
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    
    for feature, importance in sorted_features[:10]:  # Top 10
        print(f"  {feature}: {importance:.4f}")
    
    # Guardar métricas de entrenamiento
    metrics = {
        'final_accuracy': float(history.history['accuracy'][-1]),
        'final_val_accuracy': float(history.history['val_accuracy'][-1]),
        'final_loss': float(history.history['loss'][-1]),
        'final_val_loss': float(history.history['val_loss'][-1]),
        'epochs_trained': len(history.history['accuracy']),
        'feature_importance': {k: float(v) for k, v in feature_importance.items()}
    }
    
    with open(f"{model_path}_metrics.json", 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n✅ Entrenamiento completado!")
    print(f"Precisión final: {metrics['final_accuracy']:.4f}")
    print(f"Precisión en validación: {metrics['final_val_accuracy']:.4f}")
    print(f"Modelo guardado en: {model_path}")
    
    return classifier, metrics


def test_model(classifier: AlgorithmClassifier, test_cases: list):
    """Prueba el modelo entrenado con casos de prueba"""
    print("\n🧪 PRUEBAS DEL MODELO")
    print("=" * 30)
    
    for i, (code, expected) in enumerate(test_cases, 1):
        try:
            predicted, confidence = classifier.predict(code)
            correct = predicted == expected
            status = "✅" if correct else "❌"
            
            print(f"\nTest {i}: {status}")
            print(f"Esperado: {expected}")
            print(f"Predicción: {predicted}")
            print(f"Confianza: {confidence:.4f}")
            
            if not correct:
                print(f"❌ Error en la predicción")
            
        except Exception as e:
            print(f"\nTest {i}: ❌ Error - {e}")


def main():
    parser = argparse.ArgumentParser(description="Entrenar modelo de clasificación de algoritmos")
    parser.add_argument('--samples', type=int, default=100,
                       help='Muestras por clase (default: 100)')
    parser.add_argument('--epochs', type=int, default=100,
                       help='Número de épocas (default: 100)')
    parser.add_argument('--batch-size', type=int, default=32,
                       help='Tamaño del batch (default: 32)')
    parser.add_argument('--model-path', type=str, default='models/algorithm_classifier',
                       help='Ruta para guardar el modelo (default: models/algorithm_classifier)')
    parser.add_argument('--test', action='store_true',
                       help='Ejecutar pruebas después del entrenamiento')
    
    args = parser.parse_args()
    
    try:
        # Entrenar modelo
        classifier, metrics = train_model(
            samples_per_class=args.samples,
            epochs=args.epochs,
            batch_size=args.batch_size,
            model_path=args.model_path
        )
        
        # Ejecutar pruebas si se solicita
        if args.test:
            test_cases = [
                # O(1) - Constante
                ("""def get_first(arr):
    return arr[0] if arr else None""", "O(1)"),
                
                # O(n) - Lineal
                ("""def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1""", "O(n)"),
                
                # O(n²) - Cuadrático
                ("""def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr""", "O(n²)"),
                
                # O(2ⁿ) - Exponencial
                ("""def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)""", "O(2ⁿ)"),
                
                # O(n!) - Factorial
                ("""def permutations(arr):
    if len(arr) <= 1:
        return [arr]
    result = []
    for i in range(len(arr)):
        current = arr[i]
        remaining = arr[:i] + arr[i+1:]
        for perm in permutations(remaining):
            result.append([current] + perm)
    return result""", "O(n!)")
            ]
            
            test_model(classifier, test_cases)
        
        print(f"\n🎉 ¡Entrenamiento completado exitosamente!")
        print(f"El modelo está listo para usar en el analizador de algoritmos.")
        
    except Exception as e:
        print(f"❌ Error durante el entrenamiento: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 