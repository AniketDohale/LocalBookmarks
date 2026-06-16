# Changelog

⚠️ This project is currently under active development. Features and APIs may change.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [v1.5.1] - 2026-06-16

> ⚠️ This release is still under active development. Some features may be incomplete or subject to change.

### Added
- Added “Copy URL” action button in bookmark cards for quick clipboard access
- Added responsive action row behavior for better mobile usability
- Improved mobile layout of bookmark cards to prevent overflow on small screens
- Added "Copy URL" Fallback method.

### Changed
- Category and Tag names now preserve the original user-entered capitalization
- Category and Tag lookups are now case-insensitive while retaining display formatting
- URL storage now preserves the original URL casing instead of converting URLs to lowercase
- Removed URL uniqueness enforcement, allowing the same URL to be saved multiple times with different titles, tags, or categories

### Improved
- Enhanced Category and Tag matching to prevent duplicate categories regardless of capitalization
- Improved bookmark metadata consistency by preserving user-defined naming conventions

### Fixed
- Fixed Category and Tag names being automatically converted to lowercase during creation and updates
- Fixed URLs losing their original casing when bookmarks were created or edited
- Fixed Copy URL for raspberry pi

---

## [v1.5.0] - 2026-06-16

> ⚠️ This release is still under active development. Some features may be incomplete or subject to change.

### Added
- Added UI Style to Application
- Create Category modal on the home page
- Add Bookmark modal within category pages
- Update Bookmark modal within category pages
- Reusable modal open/close handlers

### Changed
- Category creation now happens without leaving the home page
- Bookmark creation and editing now happens directly from the category page
- Improved workflow by keeping users on the current page during CRUD operations
- Reused modal styling `(modal.css)` across bookmark and category management

### Fixed
- Fixed bookmark form state reset when closing modals
- Fixed modal message cleanup between operations
- Fixed bookmark update form population from API data
- Fixed page navigation interruptions during add/edit operations

### Removed
- Dedicate Add Category Page `(add_Category.html)`
- Dedicated Add Bookmark page `(add_Bookmark.html)`
- Dedicated Update Bookmark page `(update_Bookmark.html)`
- /add-category route for category creation
- /add route for bookmark creation
- /update/<bookmark_id> route for bookmark editing
- Query-string based category prefill logic for bookmark creation

---

## [v1.4.0] - 2026-06-13

> ⚠️ This release is still under active development. Some features may be incomplete or subject to change.

### Added
- Base template (base.html) with Jinja blocks (content, scripts, extra_nav)
- Modular JS structure under `static/scripts/`

### Changed
- Moved all inline JavaScript to static files
- Replaced repeated navigation with template inheritance
- Updated pages to fully use extends `base.html`

### Fixed
- Fixed missing function errors after JS modularization
- Fixed Jinja variables inside static JS files
- Fixed broken category/bookmark API integration
- Fixed DOM timing issues in external scripts
- Fixed navigation inconsistencies across pages

### Removed
- Inline `<script>` blocks from templates
- Duplicate navigation code
- Jinja usage inside static JS files

---

## [v1.3.0] - 2026-06-13

> ⚠️ This release is still under active development. Some features may be incomplete or subject to change.

### Added
- Added Category Rename API (`PUT /api/categories/<category_id>`)
- Added Category Delete API (`DELETE /api/categories/<category_id>`)
- Added frontend UI support for:
  - Rename Category (prompt-based UI)
  - Delete Category (confirmation-based UI)
- Added automatic reload of category list after update/delete actions
- Added safe handling for category-bookmark relationship during deletion

### Changed
- Improved Category model behavior:
  - Categories now support safe rename without affecting bookmarks directly
  - Bookmarks dynamically reflect updated category names via relationship
- Updated category delete behavior:
  - Deleting a category now removes all associated bookmarks (cascade delete)
- Improved frontend category rendering:
  - Categories now include `id` for UI actions (rename/delete)
- Improved API consistency across category endpoints

### Fixed
- Fixed issue where category name updates were not reflected in bookmark responses immediately
- Fixed missing category ID in frontend rendering causing inability to perform update/delete actions
- Fixed relationship handling to ensure bookmarks remain consistent after category updates
- Fixed UI refresh issues after category rename/delete operations

### Notes
- Category deletion is destructive and will permanently delete all associated bookmarks
- Rename operation is safe and only updates category name (no data loss)

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