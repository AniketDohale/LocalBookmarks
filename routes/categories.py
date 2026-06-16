from flask import Blueprint, request
from core.models import db, Category
from core.utils import response

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

    cleaned = name.strip()
    existing = Category.query.filter(db.func.lower(Category.name) == cleaned.lower()).first()

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

# Rename Category
@categories_bp.route("/api/categories/<string:category_id>", methods=["PUT"])
def rename_Category(category_id):
    category = db.session.get(Category, category_id)

    if not category:
        return response(
            success=False,
            message="Category Not Found",
            status_code=404
        )

    data = request.get_json()
    name = data.get("name")

    if not name:
        return response(
            success=False,
            message="Category Name is Required",
            status_code=400
        )

    cleaned = name.strip()
    existing = Category.query.filter(db.func.lower(Category.name) == cleaned.lower()).first()

    if existing and existing.id != category.id:
        return response(
            success=False,
            message="Category Already Exists",
            status_code=400
        )

    category.name = cleaned
    db.session.commit()

    return response(
        success=True,
        message="Category Renamed",
        data=category.to_dict()
    )

# Delete Category and Bookmarks inside it
@categories_bp.route("/api/categories/<string:category_id>", methods=["DELETE"])
def delete_Category(category_id):
    category = db.session.get(Category, category_id)

    if not category:
        return response(
            success=False,
            message="Category Not Found",
            status_code=404
        )

    db.session.delete(category)
    db.session.commit()

    return response(
        success=True,
        message="Category and Associated Bookmarks Deleted",
        data={
            "deleted_id": category_id
        }
    )