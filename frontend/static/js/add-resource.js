const BASE_URL = "http://127.0.0.1:5000";

const TOKEN = localStorage.getItem("token");

if (!TOKEN) {
    window.location.href = "login.html";
}

document.getElementById("resource-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const url = document.getElementById("url").value;
    const description = document.getElementById("description").value;

    try {
        const response = await fetch(`${BASE_URL}/resources`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${TOKEN}`
            },
            body: JSON.stringify({
                title: title,
                url: url,
                description: description
            })
        });

        const data = await response.json();
        console.log(data);

        if (response.status !== 201) {
            alert("Failed to create resource");
            return;
        }

        alert("Resource created successfully!");

        window.location.href = "dashboard.html";

    } catch (error) {
        console.error("Error creating resource:", error);
    }
});

function goBack() {
    window.location.href = "dashboard.html";
}