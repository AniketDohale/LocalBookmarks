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
                    <div class="badge-container">
                        <h3>${bookmark.title}</h3>
                        <span class="cat-badge">${bookmark.category || "None"}</span>
                    </div>
                    <p class="bookmark-text">
                        <a href="${bookmark.url}" target="_blank">
                            ${bookmark.url}
                        </a>
                    </p>
                    <div class="action-row">
                        <button onclick="copyUrl('${bookmark.url}', this)" class="icon-btn btn-copy"> 
                            <img src="/static/icons/copy.png" alt="Copy"> 
                        </button>

                        <button onclick="removeFavorite('${bookmark.id}')" class="icon-btn btn-favorite"> 
                            <img src="/static/icons/favorite.png" alt="Unfavorite">
                        </button>
                        
                        <button onclick="deleteBookmark('${bookmark.id}')" class="icon-btn btn-delete"> 
                            <img src="/static/icons/delete.png" alt="Delete">
                        </button>
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
    if (data.success) {loadFavorites();} 
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

async function copyUrl(url, btn) {
    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(url);
        } else {
            fallbackCopy(url);
        }

        if (btn) {
            const img = btn.querySelector("img");
            const originalSrc = img.src;

            img.src = "/static/icons/check.png";
            setTimeout(() => (img.src = originalSrc), 3600);
        }

    } catch (err) {
        console.error("Clipboard Error:", err);
        fallbackCopy(url);
    }
}

function fallbackCopy(url) {
    const textArea = document.createElement("textarea");
    textArea.value = url;

    textArea.style.position = "fixed";
    textArea.style.left = "-9999px";

    document.body.appendChild(textArea);
    textArea.select();

    try {
        document.execCommand("copy");
    } catch (err) {
        console.error("Copy Failed:", err);
        alert("Copy not Supported");
    }

    document.body.removeChild(textArea);
}

loadFavorites();