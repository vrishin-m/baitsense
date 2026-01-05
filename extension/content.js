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
let lastProcessedId = "";

async function initiateAIScript() {
    // 1. Get the CURRENT Video ID from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const currentVideoId = urlParams.get('v');

    // 2. If we already processed this ID, stop (prevents double triggers)
    if (!currentVideoId || currentVideoId === lastProcessedId) return;

    // 3. Wait for YouTube to update the Title to match the new video
    // We poll the DOM until the title is actually available
    let titleElement = null;
    for (let i = 0; i < 20; i++) { // Try for 10 seconds
        titleElement = document.querySelector('h1.ytd-watch-metadata yt-formatted-string');
        
        // Ensure the element exists AND isn't empty
        if (titleElement && titleElement.innerText.trim().length > 0) {
            break; 
        }
        await new Promise(r => setTimeout(r, 500));
    }

    if (titleElement) {
        lastProcessedId = currentVideoId; // Update our tracker
        const videoTitle = titleElement.innerText;
        const thumbnailUrl = `https://img.youtube.com/vi/${currentVideoId}/maxresdefault.jpg`;

        console.log("Processing NEW video:", videoTitle);
        
        // Show Loading UI
        renderPopup("AI analyzing...", "Syncing with Python...", "loading");

        // 4. Send to Python
        try {
            const response = await fetch('http://127.0.0.1:8000/process_youtube', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: videoTitle,
                    thumbnail_url: thumbnailUrl
                })
            });
            const data = await response.json();
            renderPopup("AI Result", data.summary, "success");
        } catch (error) {
            renderPopup("Error", "Check Python Terminal", "error");
        }
    }
}

// Listen for navigation
window.addEventListener('yt-navigate-finish', initiateAIScript);
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