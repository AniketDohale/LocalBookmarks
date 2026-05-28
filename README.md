# Flask Bookmark API

A simple yet powerful RESTful Bookmark Manager API built with Flask and SQLAlchemy.  
It supports CRUD operations, search, pagination, sorting, and URL validation.

---

# Features

## Core Features
- Create bookmark
- Update bookmark
- Delete bookmark
- Fetch all bookmarks

---

### Search
Search bookmarks by title or URL.

GET /api/bookmarks?q=github

---

### Pagination
Supports page-based pagination with limit control (max 50 items).

GET /api/bookmarks?page=2&limit=10

---

### Sorting
Sort bookmarks by creation time.

GET /api/bookmarks?sort=newest  
GET /api/bookmarks?sort=oldest

---

### URL Validation
- Ensures valid URLs before saving
- Requires http:// or https://

---

### Consistent API Response
```bash
{
  "success": true,
  "message": "string",
  "data": {}
}
```
---

# API Endpoints

## Create Bookmark

POST /api/bookmarks

```bash
Request:
{
  "title": "GitHub",
  "url": "https://github.com"
}
```
---

## Update Bookmark

PUT /api/bookmarks/<bookmark_id>

---

## Delete Bookmark

DELETE /api/bookmarks/<bookmark_id>

---

## Get All Bookmarks

GET /api/bookmarks

Query Params:
- q → search query
- page → page number
- limit → items per page (max 50)
- sort → newest / oldest

---

Response Example:
```bash
{
  "success": true,
  "message": "Bookmarks Fetched Successfully",
  "data": {
    "count": 10,
    "bookmarks": [],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total_items": 50,
      "total_pages": 5,
      "has_next": true,
      "has_prev": false
    }
  }
}
```
---

# Setup & Run

## Install dependencies
```bash
pip install -r requirements.txt
```
## Run application
```bash
python app.py
```
## Base URL
```bash
http://127.0.0.1:5001/api/bookmarks
```
---