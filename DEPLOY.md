# 🚀 Información de Despliegue

## URL de la Aplicación
- **Local**: http://localhost:8501
- **Producción**: [Streamlit Cloud URL]

## Comandos Útiles

### Desarrollo Local
```bash
streamlit run app.py
```

### Instalación
```bash
pip install -r requirements.txt
```

## Estructura para Despliegue
```
app_fun_car/
├── app.py              # Archivo principal
├── requirements.txt    # Dependencias
├── README.md          # Documentación
├── .streamlit/        # Configuración Streamlit
│   └── config.toml    # Tema y configuración
├── data/              # Datos de la aplicación
│   ├── cars.json      # Base de datos de autos
│   ├── questions.json # Preguntas del cuestionario
│   └── images/        # Imágenes de los autos
└── src/               # Código fuente
    ├── matcher.py     # Motor de recomendación
    ├── personality.py # Procesamiento de personalidad
    └── utils.py       # Funciones auxiliares
```

## Pasos para Desplegar en Streamlit Cloud

1. Push código a GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar repositorio GitHub
4. Seleccionar `app.py` como archivo principal
5. Deploy automático

## Funcionalidades Principales

- ✅ Cuestionario interactivo (7 preguntas)
- ✅ Motor de recomendación con algoritmo euclidiano
- ✅ Base de datos de 10 autos diversos
- ✅ Visualización con imágenes reales
- ✅ Análisis de personalidad en 5 dimensiones
- ✅ Gráficos interactivos con Plotly
- ✅ Botones para compartir en redes sociales
- ✅ Interfaz responsive y moderna
