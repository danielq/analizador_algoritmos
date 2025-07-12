#!/usr/bin/env python3
"""
Script de entrenamiento para la red neuronal del analizador de algoritmos
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from ml.neural_network import AlgorithmClassifier
from ml.dataset_generator import AlgorithmDatasetGenerator


def main():
    """Entrena la red neuronal con ejemplos de algoritmos"""
    print("🧠 ENTRENAMIENTO DE LA RED NEURONAL")
    print("=" * 50)
    
    # Crear generador de dataset
    generator = AlgorithmDatasetGenerator()
    
    # Generar datos de entrenamiento
    print("📊 Generando dataset de entrenamiento...")
    training_data = generator.generate_training_dataset()
    
    print(f"✅ Dataset generado: {len(training_data)} ejemplos")
    
    # Crear y entrenar el clasificador
    print("\n🔧 Creando clasificador...")
    classifier = AlgorithmClassifier()
    
    # Entrenar el modelo
    print("\n🚀 Iniciando entrenamiento...")
    print("Esto puede tomar unos minutos...")
    
    history = classifier.train(training_data, epochs=50, batch_size=16)
    
    # Guardar el modelo entrenado
    print("\n💾 Guardando modelo entrenado...")
    classifier.save_model("ml/trained_model")
    
    print("✅ Entrenamiento completado!")
    print("📁 Modelo guardado en: ml/trained_model")
    
    # Mostrar importancia de características
    print("\n📈 Importancia de características:")
    importance = classifier.get_feature_importance()
    for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  • {feature}: {score:.4f}")


if __name__ == "__main__":
    main() 