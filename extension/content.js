/**
 * content.js
 * Logic: Scrapes YouTube data and communicates with FastAPI
 */

// 1. Listen for YouTube's internal navigation event
window.addEventListener('yt-navigate-finish', () => {
    if (window.location.pathname === '/watch') {
        initiateAIScript();
    }
});

async function initiateAIScript() {
    // Wait for the title element to load (YouTube is slow)
    let titleElement = null;
    for (let i = 0; i < 10; i++) {
        titleElement = document.querySelector('h1.ytd-watch-metadata yt-formatted-string');
        if (titleElement && titleElement.innerText.trim() !== "") break;
        await new Promise(r => setTimeout(r, 500));
    }

    if (!titleElement) return;

    const videoId = new URLSearchParams(window.location.search).get('v');
    const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
    const videoTitle = titleElement.innerText;

    // Show initial "Processing" popup
    renderPopup("Detecting clickbait...", "Sending data to Python server...", "loading");

    try {
        const response = await fetch('http://127.0.0.1:8000/process_youtube', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: videoTitle,
                thumbnail_url: thumbnailUrl
            })
        });

        if (!response.ok) throw new Error("Server Error");

        const data = await response.json();
        
        // Update popup with real output from Python
        renderPopup("Python Result", data.summary);

    } catch (error) {
        renderPopup("Connection Error", "Is your FastAPI server running at 127.0.0.1:8000?", "error");
        console.error("Extension Error:", error);
    }
}

/**
 * UI Function: Creates and updates the floating popup
 */
function renderPopup(title, message, status) {
    let popup = document.getElementById('py-ai-popup');
    
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'py-ai-popup';
        document.body.appendChild(popup);
    }

    // Dynamic Styling
    const statusColors = {
        loading: "#3ea6ff",
        success: "#2ecc71",
        error: "#e74c3c"
    };

    Object.assign(popup.style, {
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        width: '500px',
        backgroundColor: '#1f1f1f',
        color: 'white',
        padding: '15px',
        borderRadius: '10px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
        zIndex: '10000',
        fontFamily: 'Roboto, Arial, sans-serif',
        borderLeft: `5px solid ${statusColors[status] || "#fff"}`
    });

    popup.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <b style="color:${statusColors[status]}">${title}</b>
            <span onclick="this.parentElement.parentElement.remove()" style="cursor:pointer; opacity:0.6;">✕</span>
        </div>
        <div style="font-size:16px; margin-top:8px; line-height:1.4;">${message}</div>
    `;
}