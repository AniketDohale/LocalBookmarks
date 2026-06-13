async function loadCategories() {
    const response = await fetch("/api/categories");
    const data = await response.json();

    let output = "";
    if (data.data.length === 0) {
        output = "<p>No Categories Found</p>";
    } 
    else {
        data.data.forEach(category => {
            output += `
                <div>
                    <h3>
                        <a href="/category/${category.name}">
                            ${category.name}
                        </a>
                    </h3>

                    <p>
                        Bookmarks: ${category.bookmark_count}
                    </p>

                    <button onclick="renameCategory('${category.id}', '${category.name}')">
                        Rename
                    </button>

                    <button onclick="deleteCategory('${category.id}', '${category.name}')">
                        Delete
                    </button>

                    <hr>

                </div>
            `;
        });
    }
    document.getElementById("categories").innerHTML = output;
}

async function renameCategory(id, currentName) {
    const newName = prompt("Enter new category name:", currentName);

    if (!newName || !newName.trim()) {
        return;
    }

    const response = await fetch(
        `/api/categories/${id}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: newName
            })
        }
    );

    const data = await response.json();
    alert(data.message);

    if (data.success) {
        loadCategories();
    }
}

async function deleteCategory(id, name) {
    const confirmed = confirm(
        `Delete Category "${name}"?\n\nThis will also Delete all Bookmarks in this Category.`
    );

    if (!confirmed) {
        return;
    }

    const response = await fetch(
        `/api/categories/${id}`,
        {
            method: "DELETE"
        }
    );

    const data = await response.json();
    alert(data.message);
    if (data.success) {
        loadCategories();
    }
}

loadCategories();