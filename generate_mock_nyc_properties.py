import random
import json
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

NEIGHBORHOODS = [
    "Midtown Manhattan", "Financial District", "Hudson Yards",
    "SoHo", "Tribeca", "Chelsea", "Flatiron", "Upper East Side"
]

BUILDING_CLASSES = ["A", "B", "C"]
ZONING_CODES = ["C6-1", "C6-2", "C5-3", "M1-6", "R10"]

COMPANY_SUFFIXES = ["Capital", "Partners", "Group", "Holdings", "Properties"]

def generate_company_name():
    return f"{fake.last_name()} {random.choice(COMPANY_SUFFIXES)}"

def generate_property(neighborhood):
    square_footage = random.randint(50000, 1000000)
    price_per_sqft = random.randint(300, 1200)
    sale_price = square_footage * price_per_sqft

    return {
        "property_id": fake.uuid4(),
        "address": fake.address().replace("\n", ", "),
        "neighborhood": neighborhood,
        "property_type": "Office",
        "building_class": random.choice(BUILDING_CLASSES),
        "year_built": random.randint(1920, 2022),
        "square_footage": square_footage,
        "sale_date": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime('%Y-%m-%d'),
        "sale_price": sale_price,
        "price_per_sqft": price_per_sqft,
        "buyer": generate_company_name(),
        "seller": generate_company_name(),
        "cap_rate": round(random.uniform(3.5, 6.5), 2),
        "zoning": random.choice(ZONING_CODES),
        "rental_data": {
            "asking_rent": round(random.uniform(45, 95), 2),
            "effective_rent": round(random.uniform(40, 85), 2),
            "occupancy_rate": round(random.uniform(70, 95), 1),
            "major_tenants": [generate_company_name() for _ in range(3)]
        },
        "comparable_sales": [
            {
                "comp_address": fake.address().replace("\n", ", "),
                "sale_price": random.randint(10000000, 150000000),
                "date": (datetime.now() - timedelta(days=random.randint(60, 365))).strftime('%Y-%m-%d'),
                "cap_rate": round(random.uniform(3.5, 6.5), 2)
            } for _ in range(3)
        ]
    }

def generate_properties(count=10, neighborhood="Midtown Manhattan"):
    return [generate_property(neighborhood) for _ in range(count)]

def save_to_file(data, filename="mock_properties.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10, help="Number of properties to generate")
    parser.add_argument("--neighborhood", type=str, default="Midtown Manhattan", choices=NEIGHBORHOODS)
    args = parser.parse_args()

    properties = generate_properties(count=args.count, neighborhood=args.neighborhood)
    save_to_file(properties)
    print(f"✅ Generated {args.count} properties in {args.neighborhood} and saved to mock_properties.json")