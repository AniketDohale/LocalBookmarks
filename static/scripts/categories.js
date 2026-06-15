async function loadBookmarks() {
    const categoryName = document.getElementById("bookmarks").dataset.category;

    const response = await fetch(`/api/bookmarks?category=${encodeURIComponent(categoryName)}`);
    const data = await response.json();
    let output = "";

    if (data.data.bookmarks.length === 0) {
        output = `<div class="empty">No Bookmarks Found</div>`;
    } 
    else {
        data.data.bookmarks.forEach(bookmark => {
            output += `
                <div class="card">
                    <h3>${bookmark.title}</h3>
                    <p class="bookmark-text">
                        <a href="${bookmark.url}" target="_blank">
                            ${bookmark.url}
                        </a>
                    </p>
                    <p class="bookmark-text"> Created At: ${bookmark.created_at} </p>                        
                    <p class="bookmark-text"> Updated At: ${bookmark.updated_at} </p>
                    <p class="bookmark-text">Tags: ${bookmark.tags.join(", ")}</p>
                    <div class="action-row">
                        <button onclick="openUpdateBookmarkModal('${bookmark.id}')" class="btn btn-edit"> Edit </button>
                        <button onclick="toggleFavorite('${bookmark.id}')" class="btn btn-favorite"> ${bookmark.is_favorite ? "Remove Favorite" : "Make Favorite"} </button>
                        <button onclick="deleteBookmark('${bookmark.id}')" class="btn btn-delete"> Delete </button>
                    </div>
                </div>
            `;
        });
    }
    document.getElementById("bookmarks").innerHTML = output;
}

async function toggleFavorite(bookmarkId) {
    const response = await fetch(
        `/api/bookmarks/${bookmarkId}/favorite`,
        {
            method: "PATCH"
        }
    );
    const data = await response.json();
    if (data.success) {
        loadBookmarks();
    }
}

async function deleteBookmark(bookmarkId) {
    const confirmDelete = confirm("Delete this Bookmark?");
    if (!confirmDelete) return;
    const response = await fetch(
        `/api/bookmarks/${bookmarkId}`,
        {
            method: "DELETE"
        }
    );

    const data = await response.json();
    if (data.success) {
        loadBookmarks();
    } 
    else {
        alert(data.message);
    }
}

loadBookmarks();