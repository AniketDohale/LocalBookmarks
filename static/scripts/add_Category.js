document.getElementById("categoryForm").addEventListener("submit", async function(e) {
        e.preventDefault();

        const name = document.getElementById("categoryName").value.trim();
        const response = await fetch("/api/categories", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name: name})
        });

        const data = await response.json();
        const message = document.getElementById("message");

        if (data.success) {
            message.style.color = "green";
            message.textContent = "Category Created Successfully";

            setTimeout(() => {
                window.location.href = "/";
            }, 1000);
        } 
        else {
            message.style.color = "red";
            message.textContent = data.message;
        }
    });

window.openCategoryModal = function () {
    document.getElementById("categoryModal").style.display = "flex";
    document.body.style.overflow = "hidden";
};

window.closeCategoryModal = function () {
    document.getElementById("categoryModal").style.display = "none";
    document.body.style.overflow = "";
    
    document.getElementById("message").textContent = "";
    document.getElementById("categoryForm").reset();
};

window.addEventListener("click", function (e) {
    const modal = document.getElementById("categoryModal");

    if (e.target === modal) {
        closeCategoryModal();
    }
});