# Changelog

⚠️ This project is currently under active development. Features and APIs may change.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [v1.2.0] - 2026-05-30

> ⚠️ This release is still under active development. Some features may be incomplete or subject to change.

### Added
- Added Flask Blueprints for `bookmarks` and `categories`
- Added basic frontend pages using HTML:
  - Categories page
  - Category-wise bookmarks view
  - Favorites page
  - Add bookmark page
  - Update bookmark page
- Added UI support for:
  - Favorite toggle
  - Delete bookmark
  - Update bookmark navigation

### Changed
- Refactored routes into separate files (`routes/bookmarks.py`, `routes/categories.py`)
- Updated `app.py` to use Blueprints
- Improved bookmark update logic
- Improved tag handling (`tags = data.get("tags") or []`)
- Improved URL validation and normalization

### Fixed
- Fixed DELETE route parameter mismatch
- Fixed tag crash when null value is passed
- Fixed category normalization issues

---

## [v1.1.0] - 2026-05-29

> ⚠️ This release is still under active development. Some features may be incomplete or subject to change.

### Added

- Bookmark Features
  - Added Favorite Bookmark functionality
  - Added Toggle Favorite API
  - Added Get Single Bookmark API
  - Added category support for bookmarks
  - Added bookmark-category relationship
  - Added category filtering for bookmarks
  - Added favorite filtering for bookmarks
  - Added bookmark count inside category response

- Category Features
  - Added Category model
  - Added Create Category API
  - Added Get All Categories API

- Data & Relationships
  - Added one-to-many relationship between Category and Bookmark
  - Added `is_favorite` field for bookmarks
  - Added `category_id` foreign key in bookmarks table

### Changed
- Updated bookmark response structure:
  - Added `is_favorite`
  - Added `category`
- Improved bookmark update functionality
- Improved category assignment handling
- Refactored filtering logic for better readability

---

## [v1.0.0] - 2026-05-28

> ⚠️ This release is still under active development. Some features may be incomplete or subject to change.

### Added
- Bookmark APIs:
  - Add Bookmark
  - Update Bookmark
  - Get All Bookmarks
  - Delete Bookmark
- Implemented URL validation for bookmarks
- Added search filter for bookmarks
- Added pagination support for listing bookmarks
- Added sorting functionality (Oldest / Newest)
- Standardized API response format for consistency

### Changed
- Improved overall response structure for better API consistency

### Disabled
- Bulk Bookmark API (currently disabled)

---

## Notes
- This is the initial stable release of the Bookmark API system.