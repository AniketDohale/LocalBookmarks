async function loadBookmarks() {
    const categoryName = document.getElementById("bookmarks").dataset.category;

    const response = await fetch(`/api/bookmarks?category=${encodeURIComponent(categoryName)}`);
    const data = await response.json();
    let output = "";

    if (data.data.bookmarks.length === 0) {
        output = "<p>No Bookmarks Found</p>";
    } 
    else {
        data.data.bookmarks.forEach(bookmark => {
            output += `
                <div>
                    <h2>${bookmark.title}</h2>
                    <p>
                        <a href="${bookmark.url}" target="_blank">
                            ${bookmark.url}
                        </a>
                    </p>
                    <p> Created At: ${bookmark.created_at} </p>                        
                    <p> Updated At: ${bookmark.updated_at} </p>
                    <p>Tags: ${bookmark.tags.join(", ")}</p>
                    <a href="/update/${bookmark.id}"> Edit </a>
                    <button onclick="toggleFavorite('${bookmark.id}')" > ${bookmark.is_favorite ? "Remove Favorite" : "Make Favorite"} </button>
                    <button onclick="deleteBookmark('${bookmark.id}')"> Delete </button>

                    <hr>
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