from flask import Blueprint, request
from models import db, Category
from utils import response

categories_bp = Blueprint("categories", __name__)


# Create Category
@categories_bp.route("/api/categories", methods=["POST"])
def create_Category():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return response(
            success=False,
            message="Category Name is Required",
            status_code=400
        )

    cleaned = name.strip().lower()
    existing = Category.query.filter_by(name=cleaned).first()

    if existing:
        return response(
            success=False,
            message="Category Already Exists",
            status_code=400
        )

    category = Category(name=cleaned)

    db.session.add(category)
    db.session.commit()

    return response(
        success=True,
        message="Category Created",
        data=category.to_dict(),
        status_code=201
    )

# Get Categories
@categories_bp.route("/api/categories", methods=["GET"])
def get_Categories():
    categories = Category.query.order_by(Category.name.asc()).all()

    return response(
        success=True,
        message="Categories Fetched",
        data=[c.to_dict() for c in categories]
    )