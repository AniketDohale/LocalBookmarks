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
                    <div class="card-header">
                        <a href="/category/${category.name}" class="category-name">
                            ${category.name}
                        </a>

                        <div class="right-side">
                            <span class="bookmark-count">
                                ${category.bookmark_count}
                            </span>

                            <button onclick="renameCategory('${category.id}', '${category.name}')" class="icon-btn btn-rename">
                                <img src="/static/icons/edit.png" alt="Rename">
                            </button>

                            <button onclick="deleteCategory('${category.id}', '${category.name}')" class="icon-btn btn-delete">
                                <img src="/static/icons/delete.png" alt="Delete">
                            </button>
                        </div>
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