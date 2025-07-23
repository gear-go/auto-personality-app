# Configuración para Streamlit Cloud

## Información de la App
- **Nombre**: Auto Personality App
- **Archivo principal**: app.py
- **Python version**: 3.9
- **Branch**: main

## Archivos importantes para el deploy
- `app.py` - Archivo principal de la aplicación
- `requirements.txt` - Dependencias Python
- `.python-version` - Versión de Python
- `packages.txt` - Dependencias del sistema (si es necesario)
- `.streamlit/config.toml` - Configuración del tema

## URL esperada
https://auto-personality-app.streamlit.app

## Comandos de verificación local
```bash
streamlit run app.py
```

## Troubleshooting
Si hay problemas con imágenes, verificar:
1. Rutas de archivos son relativas
2. Formatos de imagen soportados (AVIF, WebP, JPEG)
3. Tamaño de archivos no excede límites
