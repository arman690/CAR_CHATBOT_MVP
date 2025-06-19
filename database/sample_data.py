# database/sample_data.py
import sqlite3

def populate_sample_data():
    """Add sample car data to database"""
    
    sample_cars = [
        # Toyota cars
        ("Toyota", "Camry", 2024, 45000, "Sedan", "Petrol", "Automatic", 0, "نو، با تمام امکانات"),
        ("Toyota", "Camry", 2023, 42000, "Sedan", "Petrol", "Automatic", 15000, "یک ساله، خودرو ایده‌آل خانواده"),
        ("Toyota", "Corolla", 2024, 35000, "Sedan", "Petrol", "Automatic", 0, "اقتصادی و قابل اعتماد"),
        ("Toyota", "RAV4", 2023, 48000, "SUV", "Petrol", "Automatic", 20000, "SUV خانوادگی با امکانات کامل"),
        
        # BMW cars  
        ("BMW", "3 Series", 2024, 65000, "Sedan", "Petrol", "Automatic", 0, "لوکس و اسپرت"),
        ("BMW", "X3", 2023, 75000, "SUV", "Petrol", "Automatic", 12000, "SUV لوکس با تکنولوژی پیشرفته"),
        ("BMW", "5 Series", 2024, 85000, "Sedan", "Petrol", "Automatic", 0, "سدان اجرایی با بالاترین استاندارد"),
        
        # Mercedes cars
        ("Mercedes", "C-Class", 2024, 70000, "Sedan", "Petrol", "Automatic", 0, "برند آلمانی با کیفیت بالا"),
        ("Mercedes", "GLA", 2023, 68000, "SUV", "Petrol", "Automatic", 18000, "SUV کامپکت مرسدس"),
        
        # Honda cars
        ("Honda", "Civic", 2024, 38000, "Sedan", "Petrol", "Manual", 0, "ماشین جوانان، اسپرت و اقتصادی"),
        ("Honda", "CR-V", 2023, 45000, "SUV", "Petrol", "Automatic", 25000, "SUV قابل اعتماد"),
        
        # Mazda cars
        ("Mazda", "CX-5", 2024, 42000, "SUV", "Petrol", "Automatic", 0, "طراحی زیبا و عملکرد عالی"),
        ("Mazda", "3", 2023, 32000, "Hatchback", "Petrol", "Automatic", 22000, "کامپکت و زیبا"),
        
        # Hyundai cars
        ("Hyundai", "Elantra", 2024, 33000, "Sedan", "Petrol", "Automatic", 0, "گارانتی عالی و قیمت مناسب"),
        ("Hyundai", "Tucson", 2023, 44000, "SUV", "Petrol", "Automatic", 16000, "SUV با امکانات فراوان"),
        
        # Nissan cars
        ("Nissan", "Altima", 2024, 36000, "Sedan", "Petrol", "Automatic", 0, "راحتی و اقتصادی بودن"),
        ("Nissan", "X-Trail", 2023, 46000, "SUV", "Petrol", "Automatic", 21000, "SUV ۷ نفره"),
        
        # Volkswagen cars  
        ("Volkswagen", "Golf", 2024, 39000, "Hatchback", "Petrol", "Automatic", 0, "کلاسیک آلمانی"),
        ("Volkswagen", "Tiguan", 2023, 52000, "SUV", "Petrol", "Automatic", 14000, "SUV آلمانی با فناوری پیشرفته"),
        
        # Kia cars
        ("Kia", "Sportage", 2024, 41000, "SUV", "Petrol", "Automatic", 0, "طراحی مدرن، قیمت مناسب"),
    ]
    
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM cars')
    
    # Insert sample data
    cursor.executemany('''
        INSERT INTO cars (make, model, year, price, body_type, fuel_type, transmission, mileage, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_cars)
    
    conn.commit()
    conn.close()
    print(f"✅ Added {len(sample_cars)} sample cars to database")