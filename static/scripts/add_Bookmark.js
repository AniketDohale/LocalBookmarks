document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("bookmarkForm");

    if (!form) return;

    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        const payload = {
            title: document.getElementById("title").value,
            url: document.getElementById("url").value,
            category: document.getElementById("category").value,
            tags: document.getElementById("tags").value.split(",").map(tag => tag.trim()).filter(tag => tag !== "")
        };

        const response = await fetch("/api/bookmarks", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        const messageBox = document.getElementById("bookmarkMessage");

        if (data.success) {
            messageBox.style.color = "green";
            messageBox.textContent = "Bookmark Added Successfully";

            setTimeout(() => {
                closeBookmarkModal();
                location.reload();
            }, 1000);
        } 
        else {
            messageBox.style.color = "red";
            messageBox.textContent = data.message;
        }
    });
});

window.openBookmarkModal = function () {
    document.getElementById("bookmarkModal").style.display = "flex";
    document.body.style.overflow = "hidden";
};

window.closeBookmarkModal = function () {
    document.getElementById("bookmarkModal").style.display = "none";
    document.body.style.overflow = "";

    document.getElementById("bookmarkForm").reset();
    document.getElementById("bookmarkMessage").textContent = "";
};

window.addEventListener("click", function (e) {
    const modal = document.getElementById("bookmarkModal");

    if (e.target === modal) {
        closeBookmarkModal();
    }
});