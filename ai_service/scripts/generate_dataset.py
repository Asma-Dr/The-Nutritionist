import csv
import random

# Tunisian Food Data (Real + Variations)
tunisian_foods = [
    {"name": "Couscous with Lamb", "cal": 900, "p": 35, "f": 40, "c": 90, "price": 12.0, "cat": "Tunisian"},
    {"name": "Lablabi", "cal": 350, "p": 15, "f": 10, "c": 45, "price": 4.5, "cat": "Tunisian"},
    {"name": "Lablabi with Egg", "cal": 420, "p": 21, "f": 15, "c": 45, "price": 5.5, "cat": "Tunisian"},
    {"name": "Lablabi with Tuna", "cal": 450, "p": 25, "f": 15, "c": 45, "price": 6.5, "cat": "Tunisian"},
    {"name": "Ojja Merguez", "cal": 450, "p": 18, "f": 25, "c": 12, "price": 14.0, "cat": "Tunisian"},
    {"name": "Ojja Seafood", "cal": 380, "p": 25, "f": 18, "c": 10, "price": 18.0, "cat": "Tunisian"},
    {"name": "Brik a l'Oeuf", "cal": 280, "p": 10, "f": 18, "c": 15, "price": 2.5, "cat": "Tunisian"},
    {"name": "Brik Thon", "cal": 320, "p": 15, "f": 20, "c": 15, "price": 3.0, "cat": "Tunisian"},
    {"name": "Slata Mechouia", "cal": 120, "p": 4, "f": 8, "c": 10, "price": 7.0, "cat": "Tunisian"},
    {"name": "Slata Tounsiya", "cal": 90, "p": 2, "f": 5, "c": 8, "price": 5.0, "cat": "Tunisian"},
    {"name": "Kafteji", "cal": 350, "p": 8, "f": 22, "c": 25, "price": 6.0, "cat": "Tunisian"},
    {"name": "Fricasse", "cal": 400, "p": 12, "f": 25, "c": 30, "price": 2.5, "cat": "Tunisian"},
    {"name": "Makroudh", "cal": 350, "p": 3, "f": 15, "c": 50, "price": 1.5, "cat": "Tunisian"},
    {"name": "Bambalouni", "cal": 300, "p": 4, "f": 12, "c": 45, "price": 1.5, "cat": "Tunisian"},
    {"name": "Chorba Frik", "cal": 200, "p": 10, "f": 5, "c": 25, "price": 4.0, "cat": "Tunisian"},
    {"name": "Mloukhiya", "cal": 500, "p": 30, "f": 35, "c": 15, "price": 15.0, "cat": "Tunisian"},
    {"name": "Kamounia", "cal": 600, "p": 35, "f": 40, "c": 10, "price": 16.0, "cat": "Tunisian"},
    {"name": "Rouz Jerbi", "cal": 450, "p": 15, "f": 15, "c": 60, "price": 10.0, "cat": "Tunisian"},
    {"name": "Assida Zgougou", "cal": 450, "p": 8, "f": 15, "c": 70, "price": 8.0, "cat": "Tunisian"},
    {"name": "Tajine Tunisian", "cal": 350, "p": 20, "f": 25, "c": 10, "price": 4.0, "cat": "Tunisian"},
    {"name": "Mlewi", "cal": 300, "p": 8, "f": 10, "c": 45, "price": 1.5, "cat": "Tunisian"},
    {"name": "Makloub Escalope", "cal": 600, "p": 30, "f": 25, "c": 55, "price": 8.0, "cat": "Tunisian"},
    {"name": "Makloub Chawarma", "cal": 650, "p": 28, "f": 30, "c": 55, "price": 8.5, "cat": "Tunisian"},
    {"name": "Libanais", "cal": 550, "p": 25, "f": 20, "c": 50, "price": 7.0, "cat": "Tunisian"},
    {"name": "Baguette Farcie", "cal": 700, "p": 30, "f": 30, "c": 60, "price": 9.0, "cat": "Tunisian"},
    {"name": "Yo-Yo", "cal": 250, "p": 3, "f": 12, "c": 35, "price": 1.2, "cat": "Tunisian"},
    {"name": "Samsa", "cal": 200, "p": 4, "f": 10, "c": 25, "price": 2.0, "cat": "Tunisian"},
    {"name": "Kaak Warka", "cal": 150, "p": 2, "f": 8, "c": 18, "price": 1.5, "cat": "Tunisian"},
    {"name": "Zlabia", "cal": 300, "p": 1, "f": 10, "c": 55, "price": 15.0, "cat": "Tunisian"}, # price per kg often, but unit here
    {"name": "Ghraiba", "cal": 180, "p": 2, "f": 10, "c": 20, "price": 1.0, "cat": "Tunisian"},
    {"name": "Harrisa (tbsp)", "cal": 20, "p": 1, "f": 1, "c": 2, "price": 0.5, "cat": "Tunisian"},
    {"name": "Bsissa", "cal": 400, "p": 12, "f": 10, "c": 60, "price": 5.0, "cat": "Tunisian"},
    {"name": "Droo", "cal": 350, "p": 8, "f": 5, "c": 65, "price": 4.0, "cat": "Tunisian"},
    {"name": "Masfouf", "cal": 400, "p": 6, "f": 10, "c": 70, "price": 6.0, "cat": "Tunisian"},
    {"name": "Nwaser", "cal": 500, "p": 25, "f": 20, "c": 55, "price": 14.0, "cat": "Tunisian"},
    {"name": "Mosli Chicken", "cal": 450, "p": 35, "f": 20, "c": 10, "price": 12.0, "cat": "Tunisian"},
    {"name": "Mosli Lamb", "cal": 550, "p": 30, "f": 35, "c": 5, "price": 16.0, "cat": "Tunisian"},
    {"name": "Market Jelbana", "cal": 400, "p": 20, "f": 15, "c": 35, "price": 10.0, "cat": "Tunisian"},
    {"name": "Market Loubia", "cal": 350, "p": 15, "f": 10, "c": 40, "price": 8.0, "cat": "Tunisian"}
]

# Common Global Foods (Templates)
base_foods = [
    ("Apple", 52, 0.3, 0.2, 14, 2.0, "Fruit"),
    ("Banana", 89, 1.1, 0.3, 23, 3.0, "Fruit"),
    ("Orange", 47, 0.9, 0.1, 12, 2.5, "Fruit"),
    ("Chicken Breast", 165, 31, 3.6, 0, 15.0, "Meat"),
    ("Beef Steak", 250, 26, 17, 0, 25.0, "Meat"),
    ("Salmon", 208, 20, 13, 0, 30.0, "Fish"),
    ("Rice", 130, 2.7, 0.3, 28, 2.0, "Grains"),
    ("Pasta", 131, 5, 1.1, 25, 2.0, "Grains"),
    ("Bread", 265, 9, 3.2, 49, 1.0, "Grains"),
    ("Egg", 155, 13, 11, 1.1, 0.8, "Dairy"),
    ("Milk", 42, 3.4, 1, 5, 2.0, "Dairy"),
    ("Cheese", 402, 25, 33, 1.3, 20.0, "Dairy"),
    ("Yogurt", 59, 10, 0.4, 3.6, 1.5, "Dairy"),
    ("Broccoli", 34, 2.8, 0.4, 7, 4.0, "Vegetable"),
    ("Carrot", 41, 0.9, 0.2, 10, 2.0, "Vegetable"),
    ("Spinach", 23, 2.9, 0.4, 3.6, 3.0, "Vegetable"),
    ("Potato", 77, 2, 0.1, 17, 1.5, "Vegetable"),
    ("Tomato", 18, 0.9, 0.2, 3.9, 2.0, "Vegetable"),
    ("Almonds", 579, 21, 49, 22, 40.0, "Nuts"),
    ("Walnuts", 654, 15, 65, 14, 45.0, "Nuts"),
    ("Burger", 295, 17, 14, 24, 12.0, "Fast Food"),
    ("Pizza Slice", 266, 11, 10, 33, 5.0, "Fast Food"),
    ("Fries", 312, 3.4, 15, 41, 6.0, "Fast Food"),
    ("Coke", 140, 0, 0, 39, 2.0, "Drink"),
    ("Water", 0, 0, 0, 0, 1.0, "Drink"),
    ("Coffee", 1, 0.1, 0, 0, 3.0, "Drink"),
    ("Tea", 1, 0, 0, 0, 2.0, "Drink"),
    ("Chocolate", 546, 4.9, 31, 61, 20.0, "Snack"),
    ("Chips", 536, 7, 35, 53, 5.0, "Snack")
]

def generate_variations(base_food, n=5):
    name, cal, p, f, c, price, cat = base_food
    variations = []
    
    modifiers = [
        ("Large", 1.5), ("Small", 0.7), 
        ("Organic", 1.0), ("Cooked", 1.1), 
        ("Raw", 1.0), ("Spicy", 1.05),
        ("Grilled", 0.9), ("Fried", 1.4),
        ("Boiled", 1.0), ("Roasted", 1.1)
    ]
    
    for _ in range(n):
        mod_name, multiplier = random.choice(modifiers)
        new_name = f"{mod_name} {name}"
        
        # Add some random noise to macros
        var_p = round(p * multiplier * random.uniform(0.9, 1.1), 1)
        var_f = round(f * multiplier * random.uniform(0.9, 1.1), 1)
        var_c = round(c * multiplier * random.uniform(0.9, 1.1), 1)
        var_cal = round((var_p * 4) + (var_f * 9) + (var_c * 4))
        var_price = round(price * multiplier * random.uniform(0.9, 1.2), 2)
        
        variations.append((new_name, var_cal, var_p, var_f, var_c, var_price, cat))
    return variations

def main():
    with open("data/food_database.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "calories_100g", "protein_100g", "fat_100g", "carbs_100g", "price_tnd", "category"])
        
        # Write Tunisian Foods
        for food in tunisian_foods:
            writer.writerow([food["name"], food["cal"], food["p"], food["f"], food["c"], food["price"], food["cat"]])
            
        # Write Base Global Foods
        for food in base_foods:
            writer.writerow(food)
            
        # Generate Synthetic Global Foods (Big Data simulation)
        for food in base_foods:
            variations = generate_variations(food, n=20) # 20 variations per base food = ~600 items
            for var in variations:
                writer.writerow(var)
                
        print(f"Generated food database with ~{len(base_foods)*21 + len(tunisian_foods)} items.")

if __name__ == "__main__":
    main()
