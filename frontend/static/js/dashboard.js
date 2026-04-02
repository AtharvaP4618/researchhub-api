const BASE_URL = "http://127.0.0.1:5000";
let currentPage = 1;
const limit = 5;

const TOKEN = localStorage.getItem("token");

if (!TOKEN) {
    window.location.href = "login.html";
}

async function loadResources() {
    try {
        const response = await fetch(`${BASE_URL}/resources?page=${currentPage}&limit=${limit}`, {
            headers: {
                "Authorization": `Bearer ${TOKEN}`
            }
        });

        const result = await response.json();
        console.log(result);

        const { data, meta } = result;

        if (!Array.isArray(data)) {
            console.error("Unexpected response:", result);
            return;
        }

        const container = document.getElementById("resource-list");
        container.innerHTML = "";

        data.forEach(addResourceToUI);

        updatePaginationControls(meta);

    } catch (error) {
        console.error("Error fetching resources:", error);
    }
}

function updatePaginationControls(meta) {
    const pageInfo = document.getElementById("pageInfo");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    if (meta.pages === 0) {
        pageInfo.innerText = "No pages available";
        prevBtn.disabled = true;
        nextBtn.disabled = true;
        return;
    }

    pageInfo.innerText = `Page ${meta.page} of ${meta.pages}`;

    prevBtn.disabled = !meta.has_prev;
    nextBtn.disabled = !meta.has_next;
}


document.getElementById("prevBtn").addEventListener("click", function () {
    if (currentPage > 1) {
        currentPage--;
        loadResources();
    }
});

document.getElementById("nextBtn").addEventListener("click", function () {
    currentPage++;
    loadResources();
});

function toggleForm() {
    const form = document.getElementById("form-container");
    form.style.display = form.style.display === "none" ? "block" : "none";
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
                title,
                url,
                description
            })
        });

        const data = await response.json();

        if (response.status !== 201) {
            alert("Failed to create resource");
            return;
        }

        loadResources();

        document.getElementById("resource-form").reset();

        toggleForm();

    } catch (error) {
        console.error("Error:", error);
    }
});

function addResourceToUI(resource) {
    const container = document.getElementById("resource-list");

    const div = document.createElement("div");
    div.innerHTML = `
        <h3>${resource.title}</h3>
        <p>${resource.description || ""}</p>
        <a href="${resource.url}" target="_blank">Open</a>
        <hr/>
    `;

    container.prepend(div);
}

loadResources();