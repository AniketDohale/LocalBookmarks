document.addEventListener("DOMContentLoaded", function () {

    function getQueryParam(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    const form = document.getElementById("bookmarkForm");

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

        const messageBox = document.getElementById("message");

        if (data.success) {
            messageBox.innerHTML = `<p>Bookmark Added Successfully</p>`;
            form.reset();
        } else {
            messageBox.innerHTML = `<p>${data.message}</p>`;
        }
    });

    const category = getQueryParam("category");

    if (category) {
        const categoryInput = document.getElementById("category");
        categoryInput.value = category;
        categoryInput.disabled = true;
    }

});