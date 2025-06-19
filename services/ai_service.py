# services/ai_service.py - Azure OpenAI Version
import os
import json
import re
from typing import Dict, List
from openai import AzureOpenAI

class AIService:
    def __init__(self):
        # Azure OpenAI configuration
        self.api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-12-01-preview')
        self.deployment_name = os.getenv('AZURE_DEPLOYMENT_NAME', 'gpt-4.1')
        
        if not self.api_key or not self.endpoint:
            print("⚠️  Warning: Azure OpenAI credentials not set. AI features will be limited.")
            self.client = None
        else:
            try:
                self.client = AzureOpenAI(
                    api_key=self.api_key,
                    api_version=self.api_version,
                    azure_endpoint=self.endpoint
                )
                print("✅ Azure OpenAI client initialized successfully")
            except Exception as e:
                print(f"❌ Error initializing Azure OpenAI client: {e}")
                self.client = None
    
    async def process_query(self, user_message: str) -> Dict:
        """Process user query and extract intent + entities using Azure OpenAI"""
        
        if not self.client:
            # Fallback to basic parsing if no Azure OpenAI
            return self._basic_parsing(user_message)
        
        try:
            prompt = f"""
سوال کاربر: "{user_message}"

تو یک AI هستی که در نمایندگی ماشین کار می‌کنی. کاربر سوالی پرسیده.

لطفاً پاسخ رو به فرمت JSON زیر بده:

{{
    "intent": "price_inquiry|search|specs|finance|general",
    "entities": {{
        "make": "نام برند (اگه گفته)",
        "model": "نام مدل (اگه گفته)", 
        "year": سال (اگه گفته),
        "max_price": حداکثر قیمت (اگه گفته),
        "min_price": حداقل قیمت (اگه گفته),
        "body_type": "نوع بدنه (اگه گفته)"
    }},
    "confidence": عدد بین 0 تا 1
}}

مثال‌ها:
- "قیمت کمری چقدره؟" -> intent: "price_inquiry", entities: {{"make": "Toyota", "model": "Camry"}}
- "BMW زیر ۵۰ هزار دارین؟" -> intent: "search", entities: {{"make": "BMW", "max_price": 50000}}
- "ماشین خانوادگی میخوام" -> intent: "search", entities: {{"body_type": "SUV"}}

فقط JSON برگردون:
"""

            response = self.client.chat.completions.create(
                model=self.deployment_name,  # Use Azure deployment name
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                result = json.loads(ai_response)
                print(f"✅ AI Response parsed successfully: {result}")
                return result
            except json.JSONDecodeError:
                print(f"❌ Failed to parse AI response: {ai_response}")
                return self._basic_parsing(user_message)
                
        except Exception as e:
            print(f"❌ Azure OpenAI service error: {e}")
            return self._basic_parsing(user_message)
    
    def _basic_parsing(self, user_message: str) -> Dict:
        """Fallback parsing without AI"""
        message_lower = user_message.lower()
        
        # Detect intent
        intent = "general"
        if any(word in message_lower for word in ["قیمت", "چقدر", "تومان", "price"]):
            intent = "price_inquiry"
        elif any(word in message_lower for word in ["جستجو", "دارین", "میخوام", "search"]):
            intent = "search"
        elif any(word in message_lower for word in ["مشخصات", "specs", "ویژگی"]):
            intent = "specs"
        
        # Extract entities with regex
        entities = {}
        
        # Car brands (simple detection)
        brands = {
            "تویوتا": "Toyota", "toyota": "Toyota",
            "بی‌ام‌و": "BMW", "bmw": "BMW", "بی ام و": "BMW",
            "مرسدس": "Mercedes", "mercedes": "Mercedes",
            "هوندا": "Honda", "honda": "Honda",
            "مزدا": "Mazda", "mazda": "Mazda",
            "هیوندای": "Hyundai", "hyundai": "Hyundai"
        }
        
        for persian, english in brands.items():
            if persian in message_lower:
                entities["make"] = english
                break
        
        # Car models (simple detection)
        models = {
            "کمری": "Camry", "camry": "Camry",
            "کرولا": "Corolla", "corolla": "Corolla",
            "rav4": "RAV4", "راو": "RAV4"
        }
        
        for persian, english in models.items():
            if persian in message_lower:
                entities["model"] = english
                break
        
        # Price extraction
        price_match = re.search(r'(\d+)\s*(?:هزار|k|thousand)', message_lower)
        if price_match:
            entities["max_price"] = int(price_match.group(1)) * 1000
        
        print(f"📝 Basic parsing result: intent={intent}, entities={entities}")
        return {
            "intent": intent,
            "entities": entities,
            "confidence": 0.7
        }
    
    async def generate_response(self, intent: str, cars: List, user_message: str) -> str:
        """Generate natural response based on results using Azure OpenAI"""
        
        if not self.client:
            return self._basic_response(intent, cars)
        
        try:
            # Prepare context
            cars_text = ""
            if cars:
                for car in cars[:3]:
                    cars_text += f"- {car.make} {car.model} {car.year}: ${car.price:,}\n"
            
            prompt = f"""
کاربر پرسید: "{user_message}"
Intent: {intent}

ماشین‌های پیدا شده:
{cars_text if cars_text else "هیچ ماشینی پیدا نشد"}

یک پاسخ طبیعی و دوستانه به فارسی بنویس که:
- مفید و مرتبط باشه
- اگه ماشین پیدا شده، معرفی کن
- اگه پیدا نشده، گزینه‌های دیگه پیشنهاد بده  
- سوال بعدی بپرس تا بتونی بهتر کمک کنی
- حداکثر 100 کلمه

پاسخ:
"""
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            
            ai_response = response.choices[0].message.content.strip()
            print(f"✅ AI Response generated: {ai_response[:100]}...")
            return ai_response
            
        except Exception as e:
            print(f"❌ Response generation error: {e}")
            return self._basic_response(intent, cars)
    
    def _basic_response(self, intent: str, cars: List) -> str:
        """Fallback response generation"""
        if not cars:
            return "متاسفم، ماشینی با این مشخصات پیدا نکردم. میتونین مشخصات دیگه‌ای بگین؟"
        
        if intent == "price_inquiry":
            car = cars[0]
            return f"💰 {car.make} {car.model} {car.year} قیمتش ${car.price:,} هست. میخواین مشخصات بیشتری ببینین؟"
        
        elif intent == "search":
            if len(cars) == 1:
                car = cars[0]
                return f"🚗 {car.make} {car.model} {car.year} رو پیدا کردم به قیمت ${car.price:,}. علاقه‌مندین؟"
            else:
                response = f"🔍 {len(cars)} ماشین پیدا کردم:\n"
                for car in cars[:3]:
                    response += f"• {car.make} {car.model} - ${car.price:,}\n"
                return response
        
        else:
            car = cars[0]
            return f"🚗 {car.make} {car.model} {car.year} - ${car.price:,}\n{car.description}"