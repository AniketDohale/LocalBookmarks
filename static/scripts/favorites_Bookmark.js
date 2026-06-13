async function loadFavorites() {
    const response = await fetch("/api/bookmarks?favorite=true");

    const data = await response.json();
    let output = "";

    if (data.data.bookmarks.length === 0) {
        output = "<p>No Favorite Bookmarks Found</p>";
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

                    <p>
                        Category: ${bookmark.category || "None"}
                    </p>

                    <button onclick="removeFavorite('${bookmark.id}')"> Remove Favorite </button>

                    <hr>

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