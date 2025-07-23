"""
🚗 Auto Personality App
Una aplicación divertida que encuentra tu auto ideal basándose en tu personalidad
"""

import streamlit as st
import json
import numpy as np
from pathlib import Path
import sys

# Agregar src al path para imports
sys.path.append(str(Path(__file__).parent / "src"))

from matcher import AutoMatcher
from personality import PersonalityProcessor
from utils import load_json_data, display_car_result, create_car_card, generate_share_text

# Configuración de la página
st.set_page_config(
    page_title="🚗 Auto Personality App",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .question-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .result-card {
        background: #fff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .alternative-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    .share-button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 5px;
        margin: 0.25rem;
        text-decoration: none;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🚗 Auto Personality App</h1>
        <p>Descubre tu auto ideal basado en tu personalidad</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
    
    # Cargar datos
    try:
        questions_data = load_json_data("data/questions.json")
        cars_data = load_json_data("data/cars.json")
        
        if not questions_data or not cars_data:
            st.error("No se pudieron cargar los datos. Por favor, verifica que los archivos JSON existan.")
            return
            
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return
    
    # Mostrar resultado si ya se completó el cuestionario
    if st.session_state.show_result:
        show_results(st.session_state.answers, cars_data, questions_data)
        return
    
    # Mostrar cuestionario
    show_questionnaire(questions_data)

def show_questionnaire(questions_data):
    """Muestra el cuestionario interactivo"""
    
    questions = questions_data.get('questions', [])
    current_q = st.session_state.current_question
    
    if current_q >= len(questions):
        st.session_state.show_result = True
        st.rerun()
        return
    
    question = questions[current_q]
    
    # Barra de progreso
    progress = (current_q + 1) / len(questions)
    st.progress(progress)
    st.caption(f"Pregunta {current_q + 1} de {len(questions)}")
    
    # Pregunta actual
    st.markdown(f"""
    <div class="question-card">
        <h3>{question['text']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Opciones de respuesta
    options = question.get('options', [])
    
    # Usar radio buttons para las opciones
    option_texts = [opt['text'] for opt in options]
    selected = st.radio(
        "Selecciona tu respuesta:",
        options=option_texts,
        key=f"q_{current_q}"
    )
    
    # Botones de navegación
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_q > 0:
            if st.button("⬅️ Anterior"):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col3:
        if selected:
            if st.button("Siguiente ➡️"):
                # Guardar respuesta
                selected_index = option_texts.index(selected)
                selected_option = options[selected_index]
                
                if len(st.session_state.answers) <= current_q:
                    st.session_state.answers.append(selected_option)
                else:
                    st.session_state.answers[current_q] = selected_option
                
                st.session_state.current_question += 1
                st.rerun()

def show_results(answers, cars_data, questions_data):
    """Muestra los resultados de la recomendación"""
    
    # Procesar personalidad
    processor = PersonalityProcessor()
    personality_vector = processor.calculate_personality_vector(answers)
    
    # Encontrar coincidencias
    matcher = AutoMatcher(cars_data)
    recommendations = matcher.find_best_matches(personality_vector, top_n=3)
    
    if not recommendations:
        st.error("No se pudieron generar recomendaciones.")
        return
    
    # Mostrar auto principal
    best_match = recommendations[0]
    
    st.markdown("## 🎉 ¡Tu Auto Ideal!")
    
    # Usar la nueva función para mostrar la tarjeta del auto
    create_car_card(best_match['car'], best_match['match_percentage'])
    
    # Insights de personalidad
    insights = processor.generate_personality_insights(personality_vector)
    st.markdown(f"""
    ### 🧠 Insights de tu personalidad:
    {insights}
    """)
    
    # Mostrar vector de personalidad
    with st.expander("📊 Ver tu perfil de personalidad"):
        dimensions = ["Sostenibilidad", "Prestaciones", "Lujo y Confort", "Versatilidad", "Tech-savvy"]
        
        col1, col2 = st.columns(2)
        with col1:
            for i, (dim, score) in enumerate(zip(dimensions, personality_vector)):
                progress = score / 5.0
                st.metric(dim, f"{score:.1f}/5.0")
                st.progress(progress)
        
        with col2:
            # Gráfico de radar (simplificado)
            import plotly.graph_objects as go
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=personality_vector,
                theta=dimensions,
                fill='toself',
                name='Tu personalidad'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )),
                showlegend=False,
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Alternativas
    if len(recommendations) > 1:
        st.markdown("## 🚗 Otras excelentes opciones para ti:")
        
        # Mostrar alternativas en columnas
        cols = st.columns(min(len(recommendations[1:]), 2))
        
        for idx, rec in enumerate(recommendations[1:]):
            with cols[idx % len(cols)]:
                st.markdown(f"""
                <div class="alternative-card">
                    <h4>{rec['car']['emoji']} {rec['car']['brand']} {rec['car']['model']}</h4>
                    <p><strong>Match: {rec['match_percentage']:.1f}%</strong></p>
                    <p>{rec['car']['type']}</p>
                    <p style="font-size: 0.9em;">{rec['car']['description'][:100]}...</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Botones para compartir
    st.markdown("## 📱 ¡Comparte tu resultado!")
    
    share_text = generate_share_text(best_match['car'], best_match['match_percentage'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Botón para X (anteriormente Twitter)
        import urllib.parse
        encoded_text = urllib.parse.quote(share_text)
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
        # Copiar al portapapeles
        if st.button("📋 Ver texto para copiar", key="copy_text"):
            st.text_area("Copia este texto:", share_text, height=100, key="share_text_display")
    
    with col3:
        # Botón para Facebook
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
    
    # Mostrar URLs para debug (puedes quitar esto después)
    with st.expander("� Ver enlaces generados (debug)"):
        st.write("**X (Twitter):**")
        st.code(x_url)
        st.write("**Facebook:**")
        st.code(fb_url)
    
    # Botón para reiniciar
    st.markdown("---")
    if st.button("🔄 Hacer el test de nuevo", key="restart_button"):
        # Reiniciar session state
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.show_result = False
        st.rerun()

if __name__ == "__main__":
    main()
