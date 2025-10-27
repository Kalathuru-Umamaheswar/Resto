from app import app, db, Restaurant, MenuItem

# This script seeds the SQLite DB with 10 restaurants and 15 menu items each.
RESTAURANTS = [
    {"name": "Pizza Palace", "cuisine": "Italian, Pizza", "rating": 4.6, "image": "https://images.unsplash.com/photo-1603078261713-9b1f8b5148d4?auto=format&fit=crop&w=800&q=80"},
    {"name": "Burger Hub", "cuisine": "American, Burgers", "rating": 4.4, "image": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=800&q=80"},
    {"name": "Sushi Central", "cuisine": "Japanese, Sushi", "rating": 4.7, "image": "https://images.unsplash.com/photo-1553621042-f6e147245754?auto=format&fit=crop&w=800&q=80"},
    {"name": "Curry Corner", "cuisine": "Indian, Curry", "rating": 4.5, "image": "https://images.unsplash.com/photo-1604908177522-9d0b9e1b8b6a?auto=format&fit=crop&w=800&q=80"},
    {"name": "Taco Town", "cuisine": "Mexican, Tacos", "rating": 4.3, "image": "https://images.unsplash.com/photo-1601924582975-38b6953e44a6?auto=format&fit=crop&w=800&q=80"},
    {"name": "Noodle Nest", "cuisine": "Chinese, Noodles", "rating": 4.2, "image": "https://images.unsplash.com/photo-1543353071-087092ec393f?auto=format&fit=crop&w=800&q=80"},
    {"name": "Green Bowl", "cuisine": "Healthy, Bowls", "rating": 4.5, "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80"},
    {"name": "Mediterraneo", "cuisine": "Mediterranean", "rating": 4.4, "image": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=800&q=80"},
    {"name": "Thai Spice", "cuisine": "Thai", "rating": 4.3, "image": "https://images.unsplash.com/photo-1546554137-f86b9593a222?auto=format&fit=crop&w=800&q=80"},
    {"name": "Sweet Tooth", "cuisine": "Desserts", "rating": 4.8, "image": "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80"},
]

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        restaurants = []
        for rdata in RESTAURANTS:
            r = Restaurant(name=rdata['name'], cuisine=rdata['cuisine'], rating=rdata['rating'], image=rdata['image'])
            restaurants.append(r)
        db.session.add_all(restaurants)
        db.session.commit()

        # Food image collections by cuisine type
        FOOD_IMAGES = {
            'Pizza': [
                'https://images.unsplash.com/photo-1604382355076-af4b0eb60143?w=800',
                'https://images.unsplash.com/photo-1513104890138-7c749659591?w=800',
                'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800',
                'https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=800',
            ],
            'Burger': [
                'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800',
                'https://images.unsplash.com/photo-1586816001966-79b736744398?w=800',
                'https://images.unsplash.com/photo-1550317138-10000687a72b?w=800',
            ],
            'Sushi': [
                'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800',
                'https://images.unsplash.com/photo-1553621042-f6e147245754?w=800',
                'https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=800',
            ],
            'Indian': [
                'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800',
                'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800',
                'https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a?w=800',
            ],
            'Mexican': [
                'https://images.unsplash.com/photo-1552332386-f8dd00dc2f85?w=800',
                'https://images.unsplash.com/photo-1625167171534-1c606d750ida?w=800',
                'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800',
            ],
            'Chinese': [
                'https://images.unsplash.com/photo-1552611052-33e04de081de?w=800',
                'https://images.unsplash.com/photo-1569058242567-93de6c36f8f6?w=800',
                'https://images.unsplash.com/photo-1541696490-8744a5dc0228?w=800',
            ],
            'Healthy': [
                'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800',
                'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800',
                'https://images.unsplash.com/photo-1607532941433-304659e8198a?w=800',
            ],
            'Mediterranean': [
                'https://images.unsplash.com/photo-1594491690437-1f2a4e9eff72?w=800',
                'https://images.unsplash.com/photo-1599394407172-a0f87e906e25?w=800',
                'https://images.unsplash.com/photo-1642434177155-14b1dad0d815?w=800',
            ],
            'Thai': [
                'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=800',
                'https://images.unsplash.com/photo-1562565652-a0d8f0c59eb4?w=800',
                'https://images.unsplash.com/photo-1552612697-197e0e09b7b3?w=800',
            ],
            'Desserts': [
                'https://images.unsplash.com/photo-1551024601-bec78aea704b?w=800',
                'https://images.unsplash.com/photo-1587314168485-3236d6710814?w=800',
                'https://images.unsplash.com/photo-1561087538-6d38d49cb897?w=800',
            ],
        }

        # Create 15 menu items per restaurant
        menu_items = []
        for idx, r in enumerate(restaurants, start=1):
            cuisine = r.cuisine.split(',')[0]
            cuisine_key = next((k for k in FOOD_IMAGES.keys() if k.lower() in cuisine.lower()), 'Healthy')
            images = FOOD_IMAGES[cuisine_key]
            
            for i in range(1, 16):
                name = f"{cuisine} Special {i}"
                if i <= len(images):  # Use curated images first
                    img = images[i-1]
                else:  # Cycle through available images
                    img = images[(i-1) % len(images)]
                
                desc = f"Delicious {cuisine.lower()} dish made with premium ingredients. A house specialty."
                price = round(8.99 + i * 0.85 + idx * 0.5, 2)  # Base price $8.99
                menu_items.append(MenuItem(
                    name=name,
                    description=desc,
                    price=price,
                    image=img,
                    restaurant_id=r.id
                ))

        db.session.add_all(menu_items)
        db.session.commit()

        print(f"Seeded {len(restaurants)} restaurants with {len(menu_items)} menu items total.")

if __name__ == '__main__':
    seed()
