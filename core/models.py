import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Association Table
bookmark_tags = db.Table(
    "bookmark_tags",

    db.Column(
        "bookmark_id",
        db.String(36),
        db.ForeignKey("bookmarks.id"),
        primary_key=True
    ),

    db.Column(
        "tag_id",
        db.String(36),
        db.ForeignKey("tags.id"),
        primary_key=True
    )
)

# Bookmark
class Bookmark(db.Model):
    __tablename__ = "bookmarks"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    url = db.Column(
        db.String(1000),
        nullable=False,
        unique=True
    )

    is_favorite = db.Column(
        db.Boolean,
        default=False
    )

    category_id = db.Column(
        db.String(36),
        db.ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    tags = db.relationship(
        "Tag",
        secondary=bookmark_tags,
        backref="bookmarks"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "is_favorite": self.is_favorite,
            "category": self.category.name if self.category else None,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M") if self.updated_at else None,
            "tags": [tag.name for tag in self.tags]
        }
    
# Tags
class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
# Category
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    bookmarks = db.relationship(
        "Bookmark",
        backref="category",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bookmark_count": len(self.bookmarks)
        }