"""
Motor de recomendación para Auto Personality App
"""

import numpy as np
from typing import List, Dict, Any, Optional

class AutoMatcher:
    """
    Clase para encontrar coincidencias entre personalidad del usuario y autos disponibles
    """
    
    def __init__(self, cars_data: Dict[str, Any]):
        """
        Inicializa el matcher con datos de autos
        
        Args:
            cars_data (Dict[str, Any]): Datos de autos cargados desde JSON
        """
        self.cars_data = cars_data
        self.cars = cars_data.get('cars', [])
        
        # Validar datos de autos
        self._validate_car_data()
    
    def _validate_car_data(self) -> None:
        """
        Valida que los datos de autos tengan el formato correcto
        """
        valid_cars = []
        
        for car in self.cars:
            # Verificar campos requeridos
            required_fields = ['id', 'brand', 'model', 'vector']
            
            if all(field in car for field in required_fields):
                # Verificar que el vector tenga 5 dimensiones
                vector = car.get('vector', [])
                if isinstance(vector, list) and len(vector) == 5:
                    # Verificar que todos los elementos sean números
                    if all(isinstance(x, (int, float)) for x in vector):
                        valid_cars.append(car)
        
        self.cars = valid_cars
        
        if not self.cars:
            raise ValueError("No se encontraron autos válidos en los datos proporcionados")
    
    def calculate_match_score(self, user_vector: List[float], car_vector: List[float]) -> float:
        """
        Calcula el score de coincidencia entre usuario y auto
        
        Args:
            user_vector (List[float]): Vector de personalidad del usuario
            car_vector (List[float]): Vector de características del auto
            
        Returns:
            float: Score de coincidencia como porcentaje (0-100)
        """
        if len(user_vector) != len(car_vector):
            return 0.0
        
        # Calcular distancia euclidiana
        distance = np.sqrt(sum((u - c) ** 2 for u, c in zip(user_vector, car_vector)))
        
        # Convertir a porcentaje de similitud
        # Distancia máxima teórica: sqrt(5 * 4^2) = ~8.94
        max_distance = np.sqrt(5 * (4 ** 2))
        
        # Calcular similitud (inversa de la distancia normalizada)
        similarity = (1 - (distance / max_distance)) * 100
        
        # Asegurar que esté en el rango [0, 100]
        return max(0.0, min(100.0, similarity))
    
    def find_best_matches(self, user_vector: List[float], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Encuentra los mejores matches para un usuario
        
        Args:
            user_vector (List[float]): Vector de personalidad del usuario
            top_n (int): Número de recomendaciones a retornar
            
        Returns:
            List[Dict[str, Any]]: Lista de recomendaciones ordenadas por score
        """
        if not self.cars:
            return []
        
        recommendations = []
        
        for car in self.cars:
            car_vector = car.get('vector', [])
            match_score = self.calculate_match_score(user_vector, car_vector)
            
            recommendations.append({
                'car': car,
                'match_percentage': match_score,
                'match_score': match_score / 100.0  # Score normalizado 0-1
            })
        
        # Ordenar por score descendente
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Retornar top N
        return recommendations[:top_n]
    
    def get_car_by_id(self, car_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un auto específico por su ID
        
        Args:
            car_id (str): ID del auto a buscar
            
        Returns:
            Optional[Dict[str, Any]]: Datos del auto o None si no se encuentra
        """
        for car in self.cars:
            if car.get('id') == car_id:
                return car
        return None
    
    def filter_cars_by_criteria(self, 
                               min_match: float = 0.0,
                               car_type: Optional[str] = None,
                               price_range: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Filtra autos por criterios específicos
        
        Args:
            min_match (float): Score mínimo de match requerido
            car_type (Optional[str]): Tipo de auto a filtrar
            price_range (Optional[str]): Rango de precio a filtrar
            
        Returns:
            List[Dict[str, Any]]: Lista de autos filtrados
        """
        filtered_cars = []
        
        for car in self.cars:
            # Filtrar por tipo si se especifica
            if car_type and car.get('type', '').lower() != car_type.lower():
                continue
            
            # Filtrar por rango de precio si se especifica
            if price_range and car.get('price_range', '') != price_range:
                continue
            
            filtered_cars.append(car)
        
        return filtered_cars
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la base de datos de autos
        
        Returns:
            Dict[str, Any]: Estadísticas de la base de datos
        """
        if not self.cars:
            return {"total_cars": 0}
        
        # Contar por tipo
        types_count = {}
        brands_count = {}
        price_ranges_count = {}
        
        for car in self.cars:
            # Tipos
            car_type = car.get('type', 'Unknown')
            types_count[car_type] = types_count.get(car_type, 0) + 1
            
            # Marcas
            brand = car.get('brand', 'Unknown')
            brands_count[brand] = brands_count.get(brand, 0) + 1
            
            # Rangos de precio
            price_range = car.get('price_range', 'Unknown')
            price_ranges_count[price_range] = price_ranges_count.get(price_range, 0) + 1
        
        # Calcular promedios de vectores por dimensión
        vectors = [car.get('vector', [0, 0, 0, 0, 0]) for car in self.cars]
        avg_vector = []
        
        if vectors:
            for i in range(5):  # 5 dimensiones
                dimension_values = [v[i] if i < len(v) else 0 for v in vectors]
                avg_vector.append(sum(dimension_values) / len(dimension_values))
        
        return {
            "total_cars": len(self.cars),
            "types_distribution": types_count,
            "brands_distribution": brands_count,
            "price_ranges_distribution": price_ranges_count,
            "average_vector": avg_vector,
            "dimensions": ["Sostenibilidad", "Prestaciones", "Lujo y Confort", "Versatilidad", "Tech-savvy"]
        }
    
    def recommend_similar_cars(self, reference_car_id: str, top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Recomienda autos similares a uno de referencia
        
        Args:
            reference_car_id (str): ID del auto de referencia
            top_n (int): Número de recomendaciones
            
        Returns:
            List[Dict[str, Any]]: Lista de autos similares
        """
        reference_car = self.get_car_by_id(reference_car_id)
        
        if not reference_car:
            return []
        
        reference_vector = reference_car.get('vector', [])
        similar_cars = []
        
        for car in self.cars:
            if car.get('id') == reference_car_id:
                continue  # Saltar el auto de referencia
            
            car_vector = car.get('vector', [])
            similarity = self.calculate_match_score(reference_vector, car_vector)
            
            similar_cars.append({
                'car': car,
                'similarity_percentage': similarity,
                'similarity_score': similarity / 100.0
            })
        
        # Ordenar por similitud descendente
        similar_cars.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similar_cars[:top_n]
