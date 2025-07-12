# 🤖 Bot de Telegram - Analizador de Algoritmos

Un chatbot inteligente para Telegram que analiza la complejidad temporal de algoritmos usando inteligencia artificial.

## 🚀 Características

- ✅ **Análisis automático** de complejidad temporal
- ✅ **Soporte multi-lenguaje**: Python, JavaScript, Java, C++
- ✅ **Detección inteligente** de patrones de algoritmos
- ✅ **Red neuronal** para mejor precisión
- ✅ **Interfaz intuitiva** con botones inline
- ✅ **Ejemplos integrados** de algoritmos comunes
- ✅ **Guía de notaciones** asintóticas

## 📋 Requisitos

- Python 3.8+
- Token de bot de Telegram
- Dependencias del proyecto principal

## 🔧 Instalación

### 1. Instalar dependencias
```bash
pip install python-telegram-bot
```

### 2. Configurar el bot
```bash
python3 setup_telegram_bot.py
```

### 3. Crear bot en Telegram
1. Abre Telegram y busca `@BotFather`
2. Envía `/newbot`
3. Sigue las instrucciones para crear tu bot
4. Copia el token que te proporciona
5. Ejecuta el script de configuración

## 🚀 Uso

### Ejecutar el bot
```bash
python3 telegram_bot.py
```

### Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `/start` | Iniciar el bot |
| `/help` | Mostrar ayuda |
| `/analyze <código>` | Analizar código específico |
| `/examples` | Ver ejemplos de algoritmos |
| `/complexity` | Guía de notaciones O() |
| `/about` | Información del bot |

### Ejemplos de uso

#### 1. Análisis directo
```
/analyze def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```

#### 2. Envío de código
Simplemente envía el código del algoritmo y el bot lo analizará automáticamente.

## 📊 Lenguajes Soportados

### Python
```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

### JavaScript
```javascript
function binarySearch(arr, target) {
    let left = 0, right = arr.length - 1;
    while (left <= right) {
        let mid = Math.floor((left + right) / 2);
        if (arr[mid] === target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

### Java
```java
public int linearSearch(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}
```

### C++
```cpp
int binarySearch(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = (left + right) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

## 🧠 Inteligencia Artificial

El bot utiliza:
- **Análisis de patrones** tradicional
- **Red neuronal** entrenada con ejemplos
- **Detección AST** para análisis sintáctico
- **Clasificación automática** de complejidades

## 📈 Notaciones Asintóticas

| Notación | Descripción | Ejemplo |
|----------|-------------|---------|
| O(1) | Constante | Acceso a array |
| O(log n) | Logarítmica | Búsqueda binaria |
| O(n) | Lineal | Búsqueda lineal |
| O(n log n) | Linealítmica | Merge Sort |
| O(n²) | Cuadrática | Bubble Sort |
| O(n³) | Cúbica | Multiplicación de matrices |
| O(2ⁿ) | Exponencial | Fibonacci recursivo |
| O(n!) | Factorial | Permutaciones |

## 🔧 Configuración Avanzada

### Variables de entorno
```bash
export TELEGRAM_BOT_TOKEN="tu_token_aqui"
```

### Archivo .env
```env
TELEGRAM_BOT_TOKEN=tu_token_aqui
```

## 🐛 Solución de Problemas

### Error: "No se encontró el token"
1. Verifica que el token esté configurado
2. Ejecuta `python3 setup_telegram_bot.py`
3. Verifica el archivo `.env`

### Error: "Error de conexión"
1. Verifica que el token sea válido
2. Asegúrate de que el bot esté activo en Telegram
3. Revisa la conexión a internet

### Error: "python-telegram-bot no está instalado"
```bash
pip install python-telegram-bot
```

## 📝 Archivos del Bot

- `telegram_bot.py` - Bot principal
- `setup_telegram_bot.py` - Script de configuración
- `config.py` - Configuración del bot
- `.env` - Variables de entorno (se crea automáticamente)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🆘 Soporte

Si tienes problemas:
1. Revisa la documentación
2. Verifica los logs del bot
3. Abre un issue en GitHub

---

¡Disfruta analizando algoritmos con tu bot! 🚀 