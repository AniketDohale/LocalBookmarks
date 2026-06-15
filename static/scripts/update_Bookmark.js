document.getElementById("updateForm").addEventListener("submit", async function(event) {
        event.preventDefault();
        const bookmarkId = document.getElementById("update-bookmark-id").value;
        const payload = {
            title:
                document.getElementById("update-title").value,

            url:
                document.getElementById("update-url").value,

            category:
                document.getElementById("update-category").value,

            tags:
                document.getElementById("update-tags").value.split(",").map(tag => tag.trim()).filter(Boolean)
        };

        const response = await fetch(`/api/bookmarks/${bookmarkId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();
        const message = document.getElementById("updateMessage");
        if (data.success) {
            message.style.color = "green";
            message.textContent = "Bookmark Updated Successfully";

            setTimeout(() => {
                closeUpdateBookmarkModal();
                location.reload();
            }, 1000);
        } 
        else {
            message.style.color = "red";
            message.textContent = data.message;
        }
    });

window.openUpdateBookmarkModal = async function(bookmarkId) {
    const response = await fetch(`/api/bookmarks/${bookmarkId}`);
    const data = await response.json();
    const bookmark = data.data;

    document.getElementById("update-bookmark-id").value = bookmarkId;
    document.getElementById("update-title").value = bookmark.title || "";
    document.getElementById("update-url").value = bookmark.url || "";
    document.getElementById("update-category").value = bookmark.category || "";
    document.getElementById("update-tags").value = (bookmark.tags || []).join(", ");
    document.getElementById("updateBookmarkModal").style.display = "flex";
    document.body.style.overflow = "hidden";
};

window.closeUpdateBookmarkModal = function() {
    document.getElementById("updateBookmarkModal").style.display =  "none";
    document.body.style.overflow = "";
    document.getElementById("updateForm").reset();
    document.getElementById("updateMessage").textContent = "";
};

window.addEventListener("click", function (e) {
    const modal = document.getElementById("updateBookmarkModal");

    if (e.target === modal) {
        closeUpdateBookmarkModal();
    }
});