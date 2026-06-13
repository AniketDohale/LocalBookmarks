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