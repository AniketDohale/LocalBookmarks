from flask import Flask, request
from models import db, Bookmark
from utils import is_Valid_Url, response

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


with app.app_context():
    db.create_all()


# Add Bookmark
@app.route("/api/bookmarks", methods=["POST"])
def add_Bookmark():

    data = request.get_json()

    # CASE 1: Bulk Insert
    # if isinstance(data, list):
    #     created = []

    #     for item in data:
    #         title = item.get("title")
    #         url = item.get("url")

    #         if not title or not url:
    #             continue

    #         if not is_Valid_Url(url):
    #             continue

    #         bookmark = Bookmark(
    #             title=title,
    #             url=url.strip().lower().rstrip("/")
    #         )

    #         db.session.add(bookmark)
    #         created.append(bookmark)

    #     db.session.commit()

    #     return response(
    #         success=True,
    #         message=f"{len(created)} Bookmarks Created",
    #         data=[b.to_dict() for b in created],
    #         status_code=201
    #     )

    # CASE 2: Single Insert
    title = data.get("title")
    url = data.get("url")

    if not title or not url:
        return response(
            success=False,
            message="Title and URL are Required",
            status_code=400
        )
    
    # URL Validation
    if not is_Valid_Url(url):
        return response(
            success=False,
            message="Invalid URL. Must start with http:// or https://",
            status_code=400
        )

    bookmark = Bookmark(
        title=title,
        url = url.strip().lower().rstrip("/")
    )

    db.session.add(bookmark)
    db.session.commit()

    return response(
        success=True,
        message="Bookmark Created",
        data=bookmark.to_dict(),
        status_code=201
    )


# Update Bookmark
@app.route("/api/bookmarks/<string:bookmark_id>", methods=["PUT"])
def update_Bookmark(bookmark_id):

    bookmark = db.session.get(Bookmark, bookmark_id)

    if not bookmark:
        return response(
            success=False,
            message="Bookmark Not Found",
            status_code=404
        )
    
    data = request.get_json()

    title = data.get("title")
    url = data.get("url")

    # URL Validation
    if not is_Valid_Url(url):
        return response(
            success=False,
            message="Invalid URL. Must start with http:// or https://",
            status_code=400
        )

    if title:
        bookmark.title = title

    if url:
        bookmark.url = url.strip().lower().rstrip("/")

    db.session.commit()

    return response(
        success=True,
        message="Bookmark Updated",
        data=bookmark.to_dict()
    )


# Delete Bookmark
@app.route("/api/bookmarks/<string:bookmark_id>", methods=["DELETE"])
def delete_Bookmark(bookmark_id):

    bookmark = db.session.get(Bookmark, bookmark_id)

    if not bookmark:
        return response(
            success=False,
            message="Bookmark Not Found",
            status_code=404
        )

    db.session.delete(bookmark)
    db.session.commit()

    return response(
        success=True,
        message="Bookmark Deleted",
        data={"deleted_id": bookmark_id}
    )

# Get All Bookmarks
@app.route("/api/bookmarks", methods=["GET"])
def get_Bookmarks():

    query = request.args.get("q")

    # Pagination
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    page = max(1, page)
    limit = max(1, min(limit, 50))

    offset = (page - 1) * limit

    bookmarks_query = Bookmark.query

    # Search Filter
    if query:
        bookmarks_query = bookmarks_query.filter(
            (Bookmark.title.ilike(f"%{query}%")) |
            (Bookmark.url.ilike(f"%{query}%"))
        )
    
    total = bookmarks_query.count()

    total_pages = (total + limit - 1) // limit if total > 0 else 1

    if page > total_pages:
        return response(
            success=False,
            message=f"Page {page} does not exist. Max page is {total_pages}.",
            status_code=404,
            data={
                "bookmarks": [],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total_items": total,
                    "total_pages": total_pages,
                    "has_next": False,
                    "has_prev": total_pages > 1
                }
            }
        )

     # Sorting Bookmarks
    sort = request.args.get("sort", "newest")

    if sort == "oldest":
        bookmarks_query = bookmarks_query.order_by(Bookmark.created_at.asc())
    else:
        bookmarks_query = bookmarks_query.order_by(Bookmark.created_at.desc())

    bookmarks = bookmarks_query.offset(offset).limit(limit).all()

    if query and total == 0:
        message = f"No Bookmarks Found for '{query}'"
    elif query:
        message = f"Search Results for '{query}'"
    else:
        message = "Bookmarks Fetched Successfully"

    return response(
        success=True,
        message=message,
        data={
            "count": len(bookmarks),
            "bookmarks": [b.to_dict() for b in bookmarks],
            "pagination": {
                "page": page,
                "limit": limit,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)