"""
Procesamiento de personalidad para Auto Personality App
"""

import numpy as np
from typing import List, Dict, Any

class PersonalityProcessor:
    """
    Clase para procesar respuestas del cuestionario y calcular vectores de personalidad
    """
    
    def __init__(self):
        """
        Inicializa el procesador de personalidad
        
        Dimensiones del vector de personalidad:
        0: Sostenibilidad (consciencia ambiental)
        1: Prestaciones (búsqueda de potencia/velocidad)
        2: Lujo y Confort (preferencia por comodidades premium)
        3: Versatilidad (necesidad de funcionalidad múltiple)
        4: Tech-savvy (afinidad con la tecnología)
        """
        self.dimensions = [
            "Sostenibilidad",
            "Prestaciones", 
            "Lujo y Confort",
            "Versatilidad",
            "Tech-savvy"
        ]
        
        # Pesos por defecto para normalización
        self.dimension_weights = [1.0, 1.0, 1.0, 1.0, 1.0]
    
    def calculate_personality_vector(self, answers: List[Dict[str, Any]]) -> List[float]:
        """
        Calcula el vector de personalidad basado en las respuestas
        
        Args:
            answers (List[Dict[str, Any]]): Lista de respuestas del usuario
            
        Returns:
            List[float]: Vector de personalidad de 5 dimensiones
        """
        if not answers:
            return [2.5, 2.5, 2.5, 2.5, 2.5]  # Vector neutro
        
        # Inicializar vector con ceros
        personality_vector = [0.0] * len(self.dimensions)
        
        # Sumar pesos de todas las respuestas
        for answer in answers:
            weights = answer.get('weights', [0, 0, 0, 0, 0])
            
            # Validar que los pesos tengan el tamaño correcto
            if len(weights) == len(personality_vector):
                for i in range(len(personality_vector)):
                    personality_vector[i] += weights[i]
        
        # Normalizar dividiendo por el número de respuestas
        num_answers = len(answers)
        if num_answers > 0:
            personality_vector = [score / num_answers for score in personality_vector]
        
        # Aplicar pesos de dimensiones si están configurados
        for i in range(len(personality_vector)):
            personality_vector[i] *= self.dimension_weights[i]
        
        # Asegurar que los valores estén en el rango [1, 5]
        personality_vector = [max(1.0, min(5.0, score)) for score in personality_vector]
        
        return personality_vector
    
    def get_personality_description(self, personality_vector: List[float]) -> Dict[str, str]:
        """
        Genera descripción textual de la personalidad
        
        Args:
            personality_vector (List[float]): Vector de personalidad
            
        Returns:
            Dict[str, str]: Descripciones por dimensión
        """
        descriptions = {}
        
        for i, (dimension, score) in enumerate(zip(self.dimensions, personality_vector)):
            if score >= 4.0:
                level = "Alto"
            elif score >= 3.0:
                level = "Medio-Alto"
            elif score >= 2.0:
                level = "Medio"
            else:
                level = "Bajo"
                
            descriptions[dimension] = f"{level} ({score:.1f}/5.0)"
        
        return descriptions
    
    def get_dominant_traits(self, personality_vector: List[float], threshold: float = 3.5) -> List[str]:
        """
        Identifica los rasgos dominantes de personalidad
        
        Args:
            personality_vector (List[float]): Vector de personalidad
            threshold (float): Umbral para considerar un rasgo como dominante
            
        Returns:
            List[str]: Lista de rasgos dominantes
        """
        dominant_traits = []
        
        for i, score in enumerate(personality_vector):
            if score >= threshold:
                dominant_traits.append(self.dimensions[i])
        
        return dominant_traits
    
    def calculate_personality_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        """
        Calcula la similitud entre dos vectores de personalidad
        
        Args:
            vector1 (List[float]): Primer vector
            vector2 (List[float]): Segundo vector
            
        Returns:
            float: Similitud como porcentaje (0-100)
        """
        if len(vector1) != len(vector2):
            return 0.0
        
        # Calcular distancia euclidiana
        distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(vector1, vector2)))
        
        # Convertir a similitud (0-100%)
        # Distancia máxima teórica entre vectores [1,1,1,1,1] y [5,5,5,5,5] es ~8.94
        max_distance = np.sqrt(5 * (4 ** 2))  # 5 dimensiones, diferencia máxima 4 por dimensión
        
        similarity = (1 - (distance / max_distance)) * 100
        return max(0.0, min(100.0, similarity))
    
    def generate_personality_insights(self, personality_vector: List[float]) -> str:
        """
        Genera insights textuales sobre la personalidad
        
        Args:
            personality_vector (List[float]): Vector de personalidad
            
        Returns:
            str: Texto con insights de personalidad
        """
        dominant_traits = self.get_dominant_traits(personality_vector)
        descriptions = self.get_personality_description(personality_vector)
        
        if not dominant_traits:
            return "Tienes un perfil equilibrado, valorando todos los aspectos por igual al elegir un auto."
        
        insights = f"Tus rasgos dominantes son: {', '.join(dominant_traits)}. "
        
        # Insights específicos por combinaciones de rasgos
        if "Sostenibilidad" in dominant_traits and "Tech-savvy" in dominant_traits:
            insights += "Te inclinas hacia vehículos eléctricos o híbridos con tecnología avanzada."
        elif "Prestaciones" in dominant_traits and "Lujo y Confort" in dominant_traits:
            insights += "Buscas autos deportivos premium con alto rendimiento y comodidades."
        elif "Versatilidad" in dominant_traits:
            insights += "Priorizas la funcionalidad y practicidad en tu vehículo."
        elif "Sostenibilidad" in dominant_traits:
            insights += "El impacto ambiental es importante en tu decisión de compra."
        elif "Tech-savvy" in dominant_traits:
            insights += "Valoras la tecnología y conectividad en tu auto."
        
        return insights
    
    def export_personality_profile(self, personality_vector: List[float]) -> Dict[str, Any]:
        """
        Exporta un perfil completo de personalidad
        
        Args:
            personality_vector (List[float]): Vector de personalidad
            
        Returns:
            Dict[str, Any]: Perfil completo con todas las métricas
        """
        return {
            "vector": personality_vector,
            "descriptions": self.get_personality_description(personality_vector),
            "dominant_traits": self.get_dominant_traits(personality_vector),
            "insights": self.generate_personality_insights(personality_vector),
            "dimensions": {
                name: score for name, score in zip(self.dimensions, personality_vector)
            }
        }
