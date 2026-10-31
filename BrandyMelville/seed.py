from app import app, db, ClothingItem

with app.app_context():
    # This clears the old empty database and starts fresh
    db.drop_all()
    db.create_all()

    # Create a list of items to add
    items = [
        ClothingItem(name="Zelly Top", color="White", item_type="Tops"),
        ClothingItem(name="Christy Hoodie", color="Grey", item_type="Hoodies"),
        ClothingItem(name="Robbie Dress", color="Floral", item_type="Dresses"),
        ClothingItem(name="Connor Tank", color="Pink", item_type="Tops"),
    ]

    db.session.add_all(items)
    db.session.commit()
    print("Success! Your Brandy items are now in the database.")
