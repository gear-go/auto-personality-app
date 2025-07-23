# 🚗 Auto Personality App

> **Una aplicación divertida que encuentra tu auto ideal basándose en tu personalidad**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📝 Descripción

Auto Personality App es una aplicación web interactiva que recomienda el auto perfecto para ti basándose en tus respuestas a preguntas divertidas y curiosas sobre tu estilo de vida y preferencias.

### 🎯 Características

- **Cuestionario Interactivo**: 7 preguntas divertidas con opciones visuales
- **Sistema de Personalidad**: Evaluación en 5 dimensiones
- **Recomendaciones Personalizadas**: Algoritmo de matching inteligente
- **Resultados Visuales**: Interfaz atractiva con información detallada
- **Compartir Resultados**: Ideal para redes sociales

## 🚀 Instalación Rápida

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

```bash
# Clonar el repositorio
git clone https://github.com/gear-go/auto-personality-app.git
cd auto-personality-app

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

## 🎮 Cómo Usar

1. **Inicia la aplicación** ejecutando `streamlit run app.py`
2. **Responde el cuestionario** de 7 preguntas sobre tu personalidad
3. **Descubre tu auto ideal** con porcentaje de compatibilidad
4. **Explora alternativas** y características detalladas
5. **Comparte tus resultados** en redes sociales

## 🧠 Sistema de Personalidad

La app evalúa tu personalidad en 5 dimensiones:

- 🌱 **Sostenibilidad**: Consciencia ambiental
- 🏎️ **Prestaciones**: Búsqueda de potencia y velocidad  
- 💎 **Lujo y Confort**: Preferencia por comodidades premium
- 🛠️ **Versatilidad**: Necesidad de funcionalidad múltiple
- 📱 **Tech-savvy**: Afinidad con la tecnología

## 🚙 Catálogo de Autos

Actualmente incluye 10 modelos diversos:

- ⚡ **Tesla Model 3** - Sedán Eléctrico
- 🌿 **Toyota Prius** - Híbrido Compacto
- 🚛 **Ford F-150** - Pickup
- 🏎️ **Mazda MX-5** - Roadster Deportivo
- 🚙 **Honda CR-V** - SUV Compacto
- 🎯 **Mini Cooper** - Hatchback Premium
- 👑 **BMW Serie 3** - Sedán Premium
- 🏔️ **Jeep Wrangler** - SUV Todo Terreno
- ⚡ **Audi e-tron GT** - Gran Turismo Eléctrico
- 🌲 **Subaru Outback** - SUV Aventurero

## 🛠️ Estructura del Proyecto

```
auto-personality-app/
├── app.py                    # Aplicación principal Streamlit
├── requirements.txt          # Dependencias
├── README.md                # Esta documentación
├── plan_app.md              # Plan detallado del proyecto
├── data/
│   ├── cars.json           # Base de datos de autos
│   └── questions.json      # Preguntas del cuestionario
├── src/
│   ├── __init__.py
│   ├── matcher.py          # Motor de recomendación
│   ├── personality.py      # Procesamiento de personalidad
│   └── utils.py           # Funciones auxiliares
└── assets/
    └── images/             # Imágenes de los autos
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! 

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- Streamlit por el framework increíble
- La comunidad de Python
- Todos los contribuidores del proyecto

---

**Hecho con ❤️ para los amantes de los autos y la tecnología**

*¿Encontraste tu auto ideal? ¡Comparte tus resultados!* 🚗✨
