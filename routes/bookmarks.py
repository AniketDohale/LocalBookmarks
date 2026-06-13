from flask import Blueprint, request
from core.models import db, Bookmark, Tag, Category
from core.utils import is_Valid_Url, response

bookmarks_bp = Blueprint("bookmarks", __name__)


# Get Single Bookmark
@bookmarks_bp.route("/api/bookmarks/<string:bookmark_id>", methods=["GET"])
def get_Bookmark(bookmark_id):
    bookmark = db.session.get(Bookmark, bookmark_id)

    if not bookmark:
        return response(
            success=False,
            message="Bookmark Not Found",
            status_code=404
        )

    return response(
        success=True,
        message="Bookmark Fetched",
        data=bookmark.to_dict()
    )


# Get All Bookmarks
@bookmarks_bp.route("/api/bookmarks", methods=["GET"])
def get_Bookmarks():
    query = request.args.get("q")
    sort = request.args.get("sort", "newest")

    # Pagination
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    page = max(1, page)
    limit = max(1, min(limit, 50))
    offset = (page - 1) * limit

    tag = request.args.get("tag")
    favorite = request.args.get("favorite")
    category = request.args.get("category")

    bookmarks_query = Bookmark.query

    # Tag Filter
    if tag:
        bookmarks_query = bookmarks_query.join(Bookmark.tags).filter(
            Tag.name.ilike(f"%{tag.lower()}%")
        )
    
    # Favorite Filter
    if favorite and favorite.lower() == "true":
        bookmarks_query = bookmarks_query.filter(
            Bookmark.is_favorite == True
        )
    
    # Category Filter
    if category:
        bookmarks_query = bookmarks_query.join(Category).filter(
            Category.name.ilike(f"%{category.lower()}%")
        )

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
            message=f"Page {page} does not Exist. Max Page is {total_pages}.",
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


# Add Bookmark
@bookmarks_bp.route("/api/bookmarks", methods=["POST"])
def add_Bookmark():
    data = request.get_json()

    # CASE 1: Bulk Insert
    # if isinstance(data, list):

    #     created = []
    #     skipped = []

    #     for index, item in enumerate(data):
    #         title = item.get("title")
    #         url = item.get("url")
    #         tags_data = item.get("tags", [])
    #         category_name = item.get("category")

    #         # Validate Required Fields
    #         if not title or not url:
    #             skipped.append({
    #                 "index": index,
    #                 "reason": "Title and URL are Required"
    #             })
    #             continue

    #         # Normalize URL
    #         cleaned_url = url.strip().lower().rstrip("/")

    #         # Validate URL
    #         if not is_Valid_Url(cleaned_url):
    #             skipped.append({
    #                 "index": index,
    #                 "url": cleaned_url,
    #                 "reason": "Invalid URL"
    #             })
    #             continue

    #         # Prevent Duplicate URLs
    #         existing_bookmark = Bookmark.query.filter_by(url=cleaned_url).first()
    #         if existing_bookmark:
    #             skipped.append({
    #                 "index": index,
    #                 "url": cleaned_url,
    #                 "reason": "Bookmark already exists"
    #             })
    #             continue

    #         # Handle Category FIRST (Before creating Bookmark)
    #         category = None
    #         if category_name:
    #             cleaned_category = category_name.strip().lower()
    #             category = Category.query.filter_by(name=cleaned_category).first()

    #             if not category:
    #                 category = Category(name=cleaned_category)
    #                 db.session.add(category)

    #         # Create and Explicitly Track the Bookmark in the Session
    #         bookmark = Bookmark(
    #             title=title.strip(),
    #             url=cleaned_url,
    #             category=category
    #         )
    #         # Added Early to Avoid Autoflush Warnings
    #         db.session.add(bookmark)

    #         # Handle Tags
    #         for tag_name in tags_data:
    #             cleaned_tag = tag_name.strip().lower()
    #             if not cleaned_tag:
    #                 continue

    #             existing_tag = Tag.query.filter_by(name=cleaned_tag).first()

    #             if existing_tag:
    #                 bookmark.tags.append(existing_tag)
    #             else:
    #                 new_tag = Tag(name=cleaned_tag)
    #                 db.session.add(new_tag)
    #                 bookmark.tags.append(new_tag)

    #         created.append(bookmark)
    #     db.session.commit()

    #     return response(
    #         success=True,
    #         message=f"{len(created)} bookmarks created",
    #         data={
    #             "created": [b.to_dict() for b in created],
    #             "skipped": skipped
    #         },
    #         status_code=201
    #     )

    # CASE 2: Single Insert
    title = data.get("title")
    url = data.get("url")
    category_name = data.get("category")
    tags_data = data.get("tags") or []

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
            message="Invalid URL. Must Start with http:// or https://",
            status_code=400
        )

    normalized_url = url.strip().lower().rstrip("/")

    # Duplicate Check
    existing_bookmark = Bookmark.query.filter_by(url=normalized_url).first()
    if existing_bookmark:
        return response(
            success=False,
            message="Bookmark Already Exists",
            status_code=400
        )

    # Handle Category FIRST
    category = None
    if category_name:
        cleaned_category = category_name.strip().lower()
        category = Category.query.filter_by(name=cleaned_category).first()

        if not category:
            category = Category(name=cleaned_category)
            db.session.add(category)

    bookmark = Bookmark(
        title=title,
        url = normalized_url,
        category=category
    )
    # Tracked Before Querying Tags
    db.session.add(bookmark)

    # Add Tags
    for tag_name in tags_data:
        cleaned = tag_name.strip().lower()

        if not cleaned:
            continue

        existing_tag = Tag.query.filter_by(name=cleaned).first()
        if existing_tag:
            bookmark.tags.append(existing_tag)
        else:
            new_tag = Tag(name=cleaned)
            db.session.add(new_tag)
            bookmark.tags.append(new_tag)

    db.session.commit()

    return response(
        success=True,
        message="Bookmark Created",
        data=bookmark.to_dict(),
        status_code=201
    )


# Update Bookmark
@bookmarks_bp.route("/api/bookmarks/<string:bookmark_id>", methods=["PUT"])
def update_Bookmark(bookmark_id):
    bookmark = db.session.get(Bookmark, bookmark_id)

    if not bookmark:
        return response(
            success=False,
            message="Bookmark Not Found",
            status_code=404
        )

    data = request.get_json()

    tags_data = data.get("tags")
    title = data.get("title")
    url = data.get("url")
    category_name = data.get("category")  

    # URL Validation
    if url and not is_Valid_Url(url):
        return response(
            success=False,
            message="Invalid URL. Must start with http:// or https://",
            status_code=400
        )
    
    # Add Tags
    if tags_data is not None:
        bookmark.tags.clear()

        for tag_name in tags_data:
            cleaned = tag_name.strip().lower()

            if not cleaned:
                continue

            existing_tag = Tag.query.filter_by(name=cleaned).first()

            if existing_tag:
                bookmark.tags.append(existing_tag)
            else:
                new_tag = Tag(name=cleaned)
                db.session.add(new_tag)
                bookmark.tags.append(new_tag)
    
    # Update Category
    if category_name is not None:
        cleaned_category = category_name.strip().lower()

        if cleaned_category == "":
            bookmark.category = None
        else:
            category = Category.query.filter_by(name=cleaned_category).first()

            if not category:
                category = Category(name=cleaned_category)
                db.session.add(category)
            bookmark.category = category

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
@bookmarks_bp.route("/api/bookmarks/<string:bookmark_id>", methods=["DELETE"])
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

# Favorite Bookmark
@bookmarks_bp.route("/api/bookmarks/<string:bookmark_id>/favorite", methods=["PATCH"])
def toggle_Favorite(bookmark_id):
    bookmark = db.session.get(Bookmark, bookmark_id)

    if not bookmark:
        return response(
            success=False,
            message="Bookmark Not Found",
            status_code=404
        )

    bookmark.is_favorite = not bookmark.is_favorite
    db.session.commit()

    return response(
        success=True,
        message="Favorite Updated",
        data=bookmark.to_dict()
    )