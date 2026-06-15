from flask import Flask, render_template
from core.models import db
from routes.bookmarks import bookmarks_bp
from routes.categories import categories_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(bookmarks_bp)
app.register_blueprint(categories_bp)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/category/<string:category_name>")
def category_bookmarks_page(category_name):
    return render_template("categories.html", category_name=category_name)

@app.route("/favorites-page")
def favorites_page():
    return render_template("favorites_Bookmark.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002, debug=False)