
// ============================================
// API CONNECTION CONFIGURATION
// ============================================
const API_CONFIG = {
    BASE_URL: "http://127.0.0.1:8000",  // AI Tool Backend URL
    ENDPOINTS: {
        LOGIN: "/login",
        SIGNUP: "/signup",
        ANALYZE: "/analyze-batch/",
        HEALTH: "/health"
    }
};

// ============================================
// CONNECTION STATUS CHECK
// ============================================
let token = localStorage.getItem("token");
let isConnected = false;

document.addEventListener('DOMContentLoaded', () => {
    checkConnection();
    if (token) {
        showDashboard();
    }
});

async function checkConnection() {
    const statusText = document.getElementById('statusText');
    const dot = document.querySelector('.dot');
  
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HEALTH}`);
        if (response.ok) {
            isConnected = true;
            statusText.innerText = "AI Tool Connected";
            dot.classList.add('connected');
            dot.classList.remove('disconnected');
        } else {
            throw new Error("API not responding");
        }
    } catch (error) {
        isConnected = false;
        statusText.innerText = "AI Tool Disconnected";
        dot.classList.add('disconnected');
        dot.classList.remove('connected');
    }
}

// ============================================
// AUTHENTICATION FUNCTIONS
// ============================================
function showDashboard() {
    document.getElementById('authSection').classList.add('hidden');
    document.getElementById('dashboardSection').classList.remove('hidden');
  try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        document.getElementById('userDisplay').innerText = payload.sub;
    } catch (e) {
        logout();
    }
}

function logout() {
    localStorage.removeItem("token");
    token = null;
    location.reload();
}

async function signup() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!username || !password) {
        document.getElementById('authError').innerText = "Please fill in all fields";
        return;
    }

    try {
        const res = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.SIGNUP}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
      
        const data = await res.json();

        if (res.ok) {
            localStorage.setItem("token", data.access_token);
            token = data.access_token;
            showDashboard();
        } else {
            document.getElementById('authError').innerText = data.detail || "Signup failed";
        }
    } catch (error) {
        document.getElementById('authError').innerText = "Cannot connect to AI Tool. Is it running?";
    }
}

async function login() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!username || !password) {
        document.getElementById('authError').innerText = "Please fill in all fields";
        return;
    }
   const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const res = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.LOGIN}`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        if (res.ok) {
            localStorage.setItem("token", data.access_token);
            token = data.access_token;
            showDashboard();
        } else {
            document.getElementById('authError').innerText = data.detail || "Login failed";
        }
    } catch (error) {
        document.getElementById('authError').innerText = "Cannot connect to AI Tool. Is it running?";
    }
}
// ============================================
// FILE UPLOAD & BATCH PROCESSING
// ============================================
const fileInput = document.getElementById('fileInput');
const fileCount = document.getElementById('fileCount');
const uploadBtn = document.getElementById('uploadBtn');

fileInput.addEventListener('change', () => {
    const count = fileInput.files.length;
    fileCount.innerText = `${count} files selected`;

    if (count === 10) {
        fileCount.style.color = "green";
        fileCount.innerText += " ✓";
        uploadBtn.disabled = false;
    } else {
        fileCount.style.color = "red";
        fileCount.innerText += ` (Please select exactly 10)`;
        uploadBtn.disabled = true;
    }
});

async function uploadBatch() {
    const files = fileInput.files;

    if (files.length !== 10) {
        alert("Please select exactly 10 images!");
        return;
    }

    if (!isConnected) {
        alert("AI Tool is not connected. Please start the backend server.");
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('resultsSection').classList.add('hidden');
    uploadBtn.disabled = true;

    try {
        const res = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ANALYZE}`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData
        });

        const data = await res.json();

        document.getElementById('loading').classList.add('hidden');
        uploadBtn.disabled = false;

        if (res.ok) {
            document.getElementById('resultsSection').classList.remove('hidden');
            document.getElementById('llmText').innerText = data.llm_consolidated_analysis;

            const list = document.getElementById('samplesList');
            list.innerHTML = "";

            data.results.forEach(sample => {
                const div = document.createElement('div');
                div.className = 'sample-item';
                div.innerHTML = `
                    <strong>Sample ${sample.sample_id}:</strong>
                    <span>${sample.ocr_text || "No text detected"}</span>
                    ${sample.cloud_url ? `<a href="${sample.cloud_url}" target="_blank">[View Image]</a>` : ''}
                `;
                list.appendChild(div);
            });
        } else {
            alert("Error: " + (data.detail || "Processing failed"));
            if (data.detail === "Could not validate credentials") {
                logout();
            }
        }
    } catch (error) {
        document.getElementById('loading').classList.add('hidden');
        uploadBtn.disabled = false;
        alert("Connection error: " + error.message);
    }
}
      

