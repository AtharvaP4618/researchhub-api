const BASE_URL = "http://127.0.0.1:5000/auth";

document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch(`${BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ identifier: username, password: password })
        });

        if (!response.ok) {
            const errorText = await response.text();
            alert(`Login failed: ${errorText}`);
            return;
        }

        const data = await response.json();
        console.log(data);

        const token = data.access_token || data.token;

        if (!token) {
            alert("Login failed");
            return;
        }

        localStorage.setItem("token", token);

        window.location.href = "dashboard.html";

    } catch (error) {
        console.error("Login error:", error);
    }
});