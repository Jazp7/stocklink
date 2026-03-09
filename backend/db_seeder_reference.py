# db_seeder_reference.py — ONE-TIME USE script to populate your database
# This script connects directly to Supabase and creates sample data.

import asyncio
import random
from decimal import Decimal
from app.database import db
from app.models import providers as providers_model
from app.models import products as products_model
from app.schemas.providers import ProviderCreate
from app.schemas.products import ProductCreate

async def seed_data():
    print("🚀 Starting database seeding (20 Providers + 20 Products)...")
    
    # 1. Connect to the database pool
    await db.connect()
    
    # We acquire a connection from the pool to run our queries
    async with db.pool.acquire() as conn:
        
        # --- PHASE 1: CREATE 20 PROVIDERS ---
        print("\n📦 Phase 1: Creating 20 Providers...")
        
        provider_templates = [
            ("TechFlow Solutions", "Electronics"), ("Global Logistics Corp", "Shipping"),
            ("EcoParts Industries", "Hardware"), ("Smart Office Ltd", "Furniture"),
            ("Premium Components", "Electronics"), ("Reliable Tools & Co", "Hardware"),
            ("Future Systems", "Software"), ("BestBuild Supplies", "Construction"),
            ("Creative Designs Inc", "Marketing"), ("Rapid Resource Group", "Staffing"),
            ("Nexus Innovations", "Tech"), ("Apex Trading", "Retail"),
            ("Vanguard Electronics", "Electronics"), ("Horizon Logistics", "Shipping"),
            ("Blue Chip Hardware", "Hardware"), ("Silver Line Office", "Furniture"),
            ("Peak Performance", "Sports"), ("Standard Supplies", "General"),
            ("Core Tech Group", "IT"), ("Unity Solutions", "Consulting")
        ]

        created_provider_ids = []

        for name, cat in provider_templates:
            # Prepare the data using our Pydantic schema
            new_provider = ProviderCreate(
                name=name,
                email=f"contact@{name.lower().replace(' ', '').replace('&', 'and')}.com",
                phone=f"+1-555-01{random.randint(10, 99)}",
                address=f"{random.randint(100, 999)} Industrial Blvd",
                description=f"Leading experts in {cat} since {random.randint(1990, 2020)}."
            )
            
            # Save to database using our existing model
            record = await providers_model.create(conn, new_provider)
            created_provider_ids.append(record['id'])
            print(f"  ✓ Created Provider: {name}")

        # --- PHASE 2: CREATE 20 PRODUCTS ---
        print("\n🍎 Phase 2: Creating 20 Products...")
        
        product_templates = [
            ("Mechanical Keyboard", "Peripherals"), ("Ergonomic Mouse", "Peripherals"),
            ("4K Monitor", "Displays"), ("USB-C Docking Station", "Accessories"),
            ("Office Chair", "Furniture"), ("Standing Desk", "Furniture"),
            ("External SSD 1TB", "Storage"), ("Wireless Headphones", "Audio"),
            ("HD Webcam", "Video"), ("Laptop Stand", "Accessories"),
            ("Gaming Mouse Pad", "Accessories"), ("Thunderbolt Cable", "Accessories"),
            ("Anti-Static Mat", "Tools"), ("Printer Paper 500ct", "Office"),
            ("Ink Cartridge XL", "Office"), ("Bluetooth Speaker", "Audio"),
            ("Privacy Filter 24\"", "Accessories"), ("Cable Organizer", "Tools"),
            ("Desk Fan", "Office"), ("Microfiber Cloths", "Tools")
        ]

        for name, category in product_templates:
            # We assign each product to a random provider from the ones we just created
            random_provider_id = random.choice(created_provider_ids)
            
            new_product = ProductCreate(
                name=name,
                price=Decimal(f"{random.uniform(9.99, 599.99):.2f}"),
                stock_quantity=random.randint(5, 150),
                category=category,
                description=f"Professional grade {name.lower()} with full warranty.",
                provider_id=random_provider_id
            )
            
            # Save to database using our existing model
            record = await products_model.create(conn, new_product)
            print(f"  ✓ Created Product: {name}")

    # 3. Disconnect when finished
    await db.disconnect()
    print("\n✅ Seeding finished successfully! (40 items total created)")
    print("Check your dashboard at http://localhost:5173")

if __name__ == "__main__":
    asyncio.run(seed_data())
