async function loadFavorites() {
    const response = await fetch("/api/bookmarks?favorite=true");

    const data = await response.json();
    let output = "";

    if (data.data.bookmarks.length === 0) {
        output = `<div class="empty">No Favorite Bookmarks Found</div>`;
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

                    <p class="bookmark-text">
                        Category: ${bookmark.category || "None"}
                    </p>

                    <div class="action-row">
                        <button onclick="removeFavorite('${bookmark.id}')" class="btn btn-delete"> Remove Favorite </button>
                    </div>
                </div>
            `;
        });
    }
    document.getElementById("favorites").innerHTML = output;
}

async function removeFavorite(id) { 
    const response = await fetch( 
        `/api/bookmarks/${id}/favorite`, 
        { 
            method: "PATCH" 
        } 
    ); 

    const data = await response.json(); 
    if (data.success) { 
        loadFavorites();
        } 
    }

loadFavorites();