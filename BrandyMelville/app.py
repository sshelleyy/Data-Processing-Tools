from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. Setup the Database (it will create a file called brandy.db)
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# This part ensures the database stays in your main BrandyMelville folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "brandy.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# 2. Define your "Table" (What data are we saving?)
class ClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., "Tops"
    sub_category = db.Column(db.String(50), nullable=False)  # e.g., "Tanks"
    material = db.Column(db.String(50))  # e.g., "Cotton"


# 3. Create the database file (Run this once)
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # Get filters from the URL
    cat = request.args.get("category")
    sub = request.args.get("sub")
    color = request.args.get("color")

    query = ClothingItem.query

    if cat:
        query = query.filter_by(category=cat)
    if sub:
        query = query.filter_by(sub_category=sub)
    if color:
        query = query.filter_by(color=color)

    items = query.all()
    return render_template("index.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)
