# repositories/car_repository.py
import sqlite3
from typing import List, Optional, Dict
from database.models import Car

class CarRepository:
    def __init__(self, db_path: str = "cars.db"):
        self.db_path = db_path
    
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def get_all_cars(self) -> List[Car]:
        """Get all available cars"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM cars 
                WHERE available = 1 
                ORDER BY make, model, year DESC
            ''')
            rows = cursor.fetchall()
            return [Car.from_db_row(row) for row in rows]
    
    def get_car_by_id(self, car_id: int) -> Optional[Car]:
        """Get car by ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM cars 
                WHERE id = ? AND available = 1
            ''', (car_id,))
            row = cursor.fetchone()
            if row:
                return Car.from_db_row(row)
            return None
    
    def search_cars(self, filters: Dict) -> List[Car]:
        """Search cars with filters"""
        
        query = "SELECT * FROM cars WHERE available = 1"
        params = []
        
        # Build dynamic query based on filters
        if filters.get('make'):
            query += " AND LOWER(make) = LOWER(?)"
            params.append(filters['make'])
        
        if filters.get('model'):
            query += " AND LOWER(model) LIKE LOWER(?)"
            params.append(f"%{filters['model']}%")
        
        if filters.get('year'):
            query += " AND year = ?"
            params.append(filters['year'])
        
        if filters.get('max_price'):
            query += " AND price <= ?"
            params.append(filters['max_price'])
        
        if filters.get('min_price'):
            query += " AND price >= ?"
            params.append(filters['min_price'])
        
        if filters.get('body_type'):
            query += " AND LOWER(body_type) = LOWER(?)"
            params.append(filters['body_type'])
        
        if filters.get('fuel_type'):
            query += " AND LOWER(fuel_type) = LOWER(?)"
            params.append(filters['fuel_type'])
        
        # Add ordering
        query += " ORDER BY price ASC LIMIT 10"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [Car.from_db_row(row) for row in rows]
    
    def search_by_text(self, search_text: str) -> List[Car]:
        """Simple text search across make, model, description"""
        search_text = f"%{search_text.lower()}%"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM cars 
                WHERE available = 1 
                  AND (
                    LOWER(make) LIKE ? OR 
                    LOWER(model) LIKE ? OR 
                    LOWER(description) LIKE ?
                  )
                ORDER BY 
                  CASE 
                    WHEN LOWER(make) LIKE ? THEN 1
                    WHEN LOWER(model) LIKE ? THEN 2  
                    ELSE 3
                  END,
                  price ASC
                LIMIT 10
            ''', (search_text, search_text, search_text, search_text, search_text))
            
            rows = cursor.fetchall()
            return [Car.from_db_row(row) for row in rows]
    
    def get_cars_by_price_range(self, min_price: float, max_price: float) -> List[Car]:
        """Get cars in price range"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM cars 
                WHERE available = 1 
                  AND price BETWEEN ? AND ?
                ORDER BY price ASC
                LIMIT 15
            ''', (min_price, max_price))
            
            rows = cursor.fetchall()
            return [Car.from_db_row(row) for row in rows]
    
    def get_similar_cars(self, car: Car, limit: int = 5) -> List[Car]:
        """Get similar cars based on make and price range"""
        price_range = car.price * 0.3  # 30% price tolerance
        min_price = car.price - price_range
        max_price = car.price + price_range
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM cars 
                WHERE available = 1 
                  AND id != ?
                  AND (
                    make = ? OR 
                    body_type = ? OR
                    (price BETWEEN ? AND ?)
                  )
                ORDER BY 
                  CASE WHEN make = ? THEN 1 ELSE 2 END,
                  ABS(price - ?) ASC
                LIMIT ?
            ''', (car.id, car.make, car.body_type, min_price, max_price, 
                  car.make, car.price, limit))
            
            rows = cursor.fetchall()
            return [Car.from_db_row(row) for row in rows]