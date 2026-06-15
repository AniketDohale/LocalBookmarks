async function loadCategories() {
    const response = await fetch("/api/categories");
    const data = await response.json();

    let output = "";
    if (data.data.length === 0) {
        output = `<div class="empty">No Categories Found</div>`;
    } 
    else {
        data.data.forEach(category => {
            output += `
                <div class="card">
                    <h3>
                        <a href="/category/${category.name}">
                            <span class="category-name">${category.name}</span>
                            <span class="bookmark-count">${category.bookmark_count}</span>
                        </a>
                    </h3>                   

                    <div class="action-row">
                        <button onclick="renameCategory('${category.id}', '${category.name}')" class="btn btn-rename">
                            Rename
                        </button>

                        <button onclick="deleteCategory('${category.id}', '${category.name}')" class="btn btn-delete">
                            Delete
                        </button>
                    </div>
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