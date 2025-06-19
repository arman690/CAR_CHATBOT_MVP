# main.py - Fixed version
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any
import os

# Import our modules
from database.models import init_database
from database.sample_data import populate_sample_data
from services.ai_service import AIService
from services.car_service import CarService

# Initialize FastAPI app
app = FastAPI(title="Car Dealership MVP", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
ai_service = AIService()
car_service = CarService()

# Pydantic models for API
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    cars: list = []

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("🚀 Starting Car Dealership MVP...")
    init_database()
    populate_sample_data()
    print("✅ Database initialized")

@app.get("/")
async def serve_index():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage) -> ChatResponse:
    """Main chat endpoint that processes user messages"""
    
    try:
        user_message = message.message.strip()
        
        if not user_message:
            return ChatResponse(
                response="لطفاً سوال خود را بپرسید.",
                cars=[]
            )
        
        print(f"👤 User: {user_message}")
        
        # Process message with AI service
        ai_result = await ai_service.process_query(user_message)
        intent = ai_result.get("intent", "general")
        entities = ai_result.get("entities", {})
        confidence = ai_result.get("confidence", 0.5)
        
        print(f"🤖 AI Analysis: intent={intent}, entities={entities}, confidence={confidence}")
        
        # Search for cars based on entities
        cars = []
        if intent in ["search", "price_inquiry", "specs"] and entities:
            cars = car_service.search_cars(entities)
            print(f"🔍 Found {len(cars)} matching cars")
        
        # Generate response using AI
        ai_response = await ai_service.generate_response(intent, cars, user_message)
        print(f"💬 AI Response: {ai_response[:100]}...")
        
        # Prepare car data for frontend
        car_data = []
        for car in cars[:5]:  # Limit to 5 cars for performance
            car_data.append({
                "id": car.id,
                "make": car.make,
                "model": car.model,
                "year": car.year,
                "price": car.price,
                "body_type": car.body_type,
                "fuel_type": car.fuel_type,
                "transmission": car.transmission,
                "mileage": car.mileage,
                "description": car.description
            })
        
        return ChatResponse(
            response=ai_response,
            cars=car_data
        )
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return ChatResponse(
            response="متاسفم، خطایی رخ داده. لطفاً دوباره تلاش کنید.",
            cars=[]
        )

@app.get("/cars")
async def get_all_cars():
    """Get all available cars"""
    try:
        cars = car_service.get_all_cars()
        return {"cars": [
            {
                "id": car.id,
                "make": car.make,
                "model": car.model,
                "year": car.year,
                "price": car.price,
                "body_type": car.body_type,
                "description": car.description
            }
            for car in cars
        ]}
    except Exception as e:
        print(f"❌ Error getting cars: {e}")
        raise HTTPException(status_code=500, detail="خطا در دریافت اطلاعات خودروها")

@app.get("/cars/{car_id}")
async def get_car_details(car_id: int):
    """Get detailed information about a specific car"""
    try:
        car = car_service.get_car_by_id(car_id)
        if not car:
            raise HTTPException(status_code=404, detail="خودرو پیدا نشد")
        
        # Calculate on-road costs
        costs = car_service.calculate_basic_costs(car.price)
        
        return {
            "car": {
                "id": car.id,
                "make": car.make,
                "model": car.model,
                "year": car.year,
                "price": car.price,
                "body_type": car.body_type,
                "fuel_type": car.fuel_type,
                "transmission": car.transmission,
                "mileage": car.mileage,
                "description": car.description
            },
            "costs": costs
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting car details: {e}")
        raise HTTPException(status_code=500, detail="خطا در دریافت جزئیات خودرو")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_service": "connected" if ai_service.client else "limited",
        "database": "active"
    }

if __name__ == "__main__":
    print("🌐 Starting server...")
    print("📱 Open: http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)