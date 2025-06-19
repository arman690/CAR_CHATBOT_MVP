# services/car_service.py
from repositories.car_repository import CarRepository
from database.models import Car
from typing import List, Dict, Optional

class CarService:
    def __init__(self):
        self.car_repo = CarRepository()
    
    def get_all_cars(self) -> List[Car]:
        """Get all available cars"""
        return self.car_repo.get_all_cars()
    
    def get_car_by_id(self, car_id: int) -> Optional[Car]:
        """Get car by ID"""
        return self.car_repo.get_car_by_id(car_id)
    
    def search_cars(self, entities: Dict) -> List[Car]:
        """Search cars based on AI extracted entities"""
        
        # If no entities, return popular cars
        if not entities:
            return self.car_repo.get_all_cars()[:5]
        
        # First try exact search
        results = self.car_repo.search_cars(entities)
        
        # If no results, try flexible search
        if not results and entities:
            flexible_search = self._create_flexible_search(entities)
            results = self.car_repo.search_cars(flexible_search)
        
        # If still no results, try text search
        if not results:
            search_text = self._entities_to_text(entities)
            if search_text:
                results = self.car_repo.search_by_text(search_text)
        
        return results
    
    def _create_flexible_search(self, entities: Dict) -> Dict:
        """Create more flexible search criteria"""
        flexible = {}
        
        # Keep make if specified
        if entities.get('make'):
            flexible['make'] = entities['make']
        
        # Increase price range by 20%
        if entities.get('max_price'):
            flexible['max_price'] = entities['max_price'] * 1.2
        
        if entities.get('min_price'):
            flexible['min_price'] = entities['min_price'] * 0.8
        
        # Keep other exact criteria
        for key in ['year', 'body_type', 'fuel_type']:
            if entities.get(key):
                flexible[key] = entities[key]
        
        return flexible
    
    def _entities_to_text(self, entities: Dict) -> str:
        """Convert entities to text for fallback search"""
        search_parts = []
        
        if entities.get('make'):
            search_parts.append(entities['make'])
        
        if entities.get('model'):
            search_parts.append(entities['model'])
        
        if entities.get('body_type'):
            search_parts.append(entities['body_type'])
        
        return ' '.join(search_parts)
    
    def calculate_basic_costs(self, car_price: float, state: str = "NSW") -> Dict:
        """Calculate basic on-road costs"""
        
        # Australian state-specific costs (simplified)
        state_costs = {
            "NSW": {
                "registration": 800,
                "stamp_duty_rate": 0.032,
                "ctp_insurance": 600
            },
            "VIC": {
                "registration": 750,
                "stamp_duty_rate": 0.035,
                "ctp_insurance": 550
            },
            "QLD": {
                "registration": 680,
                "stamp_duty_rate": 0.030,
                "ctp_insurance": 400
            }
        }
        
        costs = state_costs.get(state, state_costs["NSW"])
        
        # Calculate costs
        registration = costs["registration"]
        stamp_duty = car_price * costs["stamp_duty_rate"]
        ctp_insurance = costs["ctp_insurance"]
        transfer_fee = 150
        dealer_delivery = 500
        
        # Optional comprehensive insurance estimate
        comprehensive_insurance = car_price * 0.04  # 4% annually
        
        total_additional = registration + stamp_duty + ctp_insurance + transfer_fee + dealer_delivery
        total_on_road = car_price + total_additional
        
        return {
            "base_price": car_price,
            "registration": registration,
            "stamp_duty": round(stamp_duty, 2),
            "ctp_insurance": ctp_insurance,
            "transfer_fee": transfer_fee,
            "dealer_delivery": dealer_delivery,
            "comprehensive_insurance_estimate": round(comprehensive_insurance, 2),
            "total_additional_costs": round(total_additional, 2),
            "total_on_road_price": round(total_on_road, 2)
        }