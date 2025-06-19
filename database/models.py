# database/models.py
import sqlite3
from dataclasses import dataclass
from typing import Optional

@dataclass
class Car:
    id: int
    make: str
    model: str
    year: int
    price: float
    body_type: str
    fuel_type: str
    transmission: str
    mileage: int
    description: str
    available: bool = True
    
    @classmethod
    def from_db_row(cls, row):
        """Create Car object from database row"""
        return cls(
            id=row[0],
            make=row[1],
            model=row[2],
            year=row[3],
            price=row[4],
            body_type=row[5],
            fuel_type=row[6],
            transmission=row[7],
            mileage=row[8],
            description=row[9],
            available=bool(row[10])
        )

def init_database():
    """Initialize SQLite database with tables"""
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    
    # Create cars table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            price REAL NOT NULL,
            body_type TEXT,
            fuel_type TEXT,
            transmission TEXT,
            mileage INTEGER,
            description TEXT,
            available BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_make ON cars(make)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_model ON cars(model)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_price ON cars(price)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_year ON cars(year)')
    
    conn.commit()
    conn.close()
    print("✅ Database tables created")