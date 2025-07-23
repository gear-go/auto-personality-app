"""
Utilidades y funciones auxiliares para Auto Personality App
"""

import json
import streamlit as st
from pathlib import Path
from typing import Dict, List, Any, Optional
from PIL import Image
import base64
import io

def load_json_data(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Carga datos desde un archivo JSON
    
    Args:
        file_path (str): Ruta al archivo JSON
        
    Returns:
        Dict[str, Any]: Datos cargados del archivo JSON o None si hay error
    """
    try:
        # Construir ruta absoluta
        current_dir = Path(__file__).parent.parent
        full_path = current_dir / file_path
        
        if not full_path.exists():
            st.error(f"Archivo no encontrado: {full_path}")
            return None
            
        with open(full_path, 'r', encoding='utf-8') as file:
            return json.load(file)
            
    except FileNotFoundError:
        st.error(f"No se pudo encontrar el archivo: {file_path}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error al parsear JSON en {file_path}: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error inesperado al cargar {file_path}: {str(e)}")
        return None

def display_car_result(car_data: Dict[str, Any], match_percentage: float) -> None:
    """
    Muestra los resultados de un auto recomendado
    
    Args:
        car_data (Dict[str, Any]): Datos del auto
        match_percentage (float): Porcentaje de coincidencia
    """
    st.markdown(f"""
    <div style="
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 1rem 0;
    ">
        <h2>{car_data.get('emoji', '🚗')} {car_data.get('brand', 'Unknown')} {car_data.get('model', 'Unknown')}</h2>
        <h3 style="color: #667eea;">Match: {match_percentage:.1f}%</h3>
        <p><strong>{car_data.get('type', 'Vehículo')}</strong></p>
        <p>{car_data.get('description', 'Sin descripción disponible.')}</p>
    </div>
    """, unsafe_allow_html=True)

def format_features_list(features: List[str]) -> str:
    """
    Formatea una lista de características como HTML
    
    Args:
        features (List[str]): Lista de características
        
    Returns:
        str: HTML formateado
    """
    if not features:
        return "<p>No hay características disponibles.</p>"
    
    html = "<ul style='text-align: left; margin: 1rem 0;'>"
    for feature in features:
        html += f"<li>✅ {feature}</li>"
    html += "</ul>"
    
    return html

def create_progress_bar(current: int, total: int) -> float:
    """
    Calcula el progreso para la barra de progreso
    
    Args:
        current (int): Posición actual
        total (int): Total de elementos
        
    Returns:
        float: Progreso como decimal entre 0 y 1
    """
    if total <= 0:
        return 1.0
    
    return min(current / total, 1.0)

def validate_vector_dimensions(vector: List[float], expected_length: int = 5) -> bool:
    """
    Valida que un vector tenga las dimensiones correctas
    
    Args:
        vector (List[float]): Vector a validar
        expected_length (int): Longitud esperada del vector
        
    Returns:
        bool: True si el vector es válido
    """
    return (
        isinstance(vector, list) and 
        len(vector) == expected_length and 
        all(isinstance(x, (int, float)) for x in vector)
    )

def safe_get_nested(data: Dict, keys: List[str], default: Any = None) -> Any:
    """
    Obtiene un valor anidado de un diccionario de forma segura
    
    Args:
        data (Dict): Diccionario fuente
        keys (List[str]): Lista de claves anidadas
        default (Any): Valor por defecto si no se encuentra
        
    Returns:
        Any: Valor encontrado o default
    """
    try:
        result = data
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError):
        return default

def generate_share_text(car_data: Dict[str, Any], match_percentage: float) -> str:
    """
    Genera texto para compartir en redes sociales
    
    Args:
        car_data (Dict[str, Any]): Datos del auto
        match_percentage (float): Porcentaje de coincidencia
        
    Returns:
        str: Texto formateado para compartir
    """
    brand = car_data.get('brand', 'Auto')
    model = car_data.get('model', 'Desconocido')
    emoji = car_data.get('emoji', '🚗')
    
    return f"""¡Mi auto ideal es el {emoji} {brand} {model}! 📊 Match: {match_percentage:.1f}% 🚗 ¿Cuál sería tu auto ideal? Descúbrelo en Auto Personality App #AutoPersonalityApp #MiAutoIdeal #CarLovers"""

def create_share_buttons(car_data: Dict[str, Any], match_percentage: float) -> None:
    """
    Crea botones para compartir en redes sociales
    
    Args:
        car_data (Dict[str, Any]): Datos del auto
        match_percentage (float): Porcentaje de coincidencia
    """
    share_text = generate_share_text(car_data, match_percentage)
    
    st.markdown("## 📱 ¡Comparte tu resultado!")
    
    col1, col2, col3 = st.columns(3)
    
    # URL encoding del texto
    import urllib.parse
    encoded_text = urllib.parse.quote(share_text)
    
    with col1:
        # X (anteriormente Twitter)
        x_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
        st.markdown(f"""
        <a href="{x_url}" target="_blank" style="
            display: inline-block;
            background: linear-gradient(90deg, #000000 0%, #1da1f2 100%);
            color: white;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        ">
            🚀 Compartir en X
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        # Mostrar texto para copiar
        if st.button("📋 Ver texto para copiar", key="show_text"):
            st.text_area("Copia este texto:", share_text, height=100)
    
    with col3:
        # Facebook
        app_url = "https://auto-personality-app.streamlit.app"
        fb_url = f"https://www.facebook.com/sharer/sharer.php?u={app_url}&quote={encoded_text}"
        st.markdown(f"""
        <a href="{fb_url}" target="_blank" style="
            display: inline-block;
            background: linear-gradient(90deg, #1877f2 0%, #42a5f5 100%);
            color: white;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        ">
            📘 Compartir en Facebook
        </a>
        """, unsafe_allow_html=True)

def load_car_image(image_filename: str, default_size: tuple = (400, 300)) -> Optional[Image.Image]:
    """
    Carga una imagen de auto desde la carpeta de imágenes
    
    Args:
        image_filename (str): Nombre del archivo de imagen
        default_size (tuple): Tamaño por defecto para redimensionar
        
    Returns:
        Optional[Image.Image]: Imagen cargada o None si hay error
    """
    try:
        # Construir ruta a la imagen
        current_dir = Path(__file__).parent.parent
        image_path = current_dir / "data" / "images" / image_filename
        
        if not image_path.exists():
            st.warning(f"Imagen no encontrada: {image_filename}")
            return None
        
        # Cargar y redimensionar imagen
        image = Image.open(image_path)
        
        # Convertir a RGB si es necesario (para formatos como AVIF/WebP)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionar manteniendo aspecto
        image.thumbnail(default_size, Image.Resampling.LANCZOS)
        
        return image
        
    except Exception as e:
        st.error(f"Error al cargar imagen {image_filename}: {str(e)}")
        return None

def display_car_image(car_data: Dict[str, Any], width: int = 400) -> None:
    """
    Muestra la imagen de un auto con fallback
    
    Args:
        car_data (Dict[str, Any]): Datos del auto
        width (int): Ancho de la imagen
    """
    image_filename = car_data.get('image', '')
    
    if image_filename:
        image = load_car_image(image_filename, (width, int(width * 0.75)))
        
        if image:
            st.image(image, width=width, use_container_width=False)
            return
    
    # Fallback: mostrar emoji grande si no hay imagen
    emoji = car_data.get('emoji', '🚗')
    st.markdown(f"""
    <div style="
        text-align: center; 
        font-size: 120px; 
        margin: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
    ">
        {emoji}
    </div>
    """, unsafe_allow_html=True)

def create_car_card(car_data: Dict[str, Any], match_percentage: float, show_image: bool = True) -> None:
    """
    Crea una tarjeta visual completa para mostrar un auto
    
    Args:
        car_data (Dict[str, Any]): Datos del auto
        match_percentage (float): Porcentaje de coincidencia
        show_image (bool): Si mostrar la imagen o no
    """
    # Container principal
    with st.container():
        if show_image:
            # Layout de 2 columnas para imagen y contenido
            col1, col2 = st.columns([1, 1])
            
            with col1:
                display_car_image(car_data, width=350)
            
            with col2:
                st.markdown(f"""
                <div style="padding: 1rem;">
                    <h2 style="color: #667eea; margin-bottom: 0.5rem;">
                        {car_data.get('emoji', '🚗')} {car_data.get('brand', 'Unknown')} {car_data.get('model', 'Unknown')}
                    </h2>
                    <h3 style="color: #28a745; margin-bottom: 1rem;">
                        ✨ Match: {match_percentage:.1f}%
                    </h3>
                    <p style="color: #6c757d; font-weight: 500; margin-bottom: 1rem;">
                        {car_data.get('type', 'Vehículo')} • {car_data.get('year', 'N/A')}
                    </p>
                    <p style="margin-bottom: 1.5rem;">
                        {car_data.get('description', 'Sin descripción disponible.')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Layout sin imagen
            st.markdown(f"""
            <div style="
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
                margin: 1rem 0;
            ">
                <h2 style="color: #667eea;">
                    {car_data.get('emoji', '🚗')} {car_data.get('brand', 'Unknown')} {car_data.get('model', 'Unknown')}
                </h2>
                <h3 style="color: #28a745;">Match: {match_percentage:.1f}%</h3>
                <p><strong>{car_data.get('type', 'Vehículo')}</strong></p>
                <p>{car_data.get('description', 'Sin descripción disponible.')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Características
        features = car_data.get('features', [])
        if features:
            st.markdown("### 🔧 Características principales:")
            
            # Mostrar características en columnas
            cols = st.columns(min(len(features), 3))
            for idx, feature in enumerate(features):
                with cols[idx % len(cols)]:
                    st.markdown(f"✅ {feature}")
        
        # Información adicional
        col1, col2 = st.columns(2)
        with col1:
            price_range = car_data.get('price_range', 'N/A')
            st.markdown(f"**💰 Rango de precio:** {price_range}")
        
        with col2:
            year = car_data.get('year', 'N/A')
            st.markdown(f"**📅 Año:** {year}")
