const resultCont = document.getElementById("result-container");
const resultDiv = document.getElementById("result");
const loadingDiv = document.getElementById("loading");
const btn = document.getElementById("analyze");

// 1. LOAD DATA ON OPEN
document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get(["lastAnalysis"], (result) => {
    if (result.lastAnalysis) {
      displayResults(result.lastAnalysis);
    }
  });
});

// 2. FETCH AND SAVE DATA
btn.addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
  const videoUrl = tab.url;

  if (!videoUrl || !videoUrl.includes("youtube.com/watch")) {
    resultDiv.innerHTML = "⚠️ Open a YouTube video.";
    resultCont.classList.remove("hidden");
    return;
  }

  loadingDiv.classList.remove("hidden");
  resultCont.classList.add("hidden");
  btn.disabled = true;

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: videoUrl })
    });

    const data = await response.json();

    if (data.success) {
      // SAVE to storage
      chrome.storage.local.set({ lastAnalysis: data.data });
      displayResults(data.data);
    } else {
      resultDiv.innerText = "Error: " + data.error;
      resultCont.classList.remove("hidden");
    }
  } catch (err) {
    resultDiv.innerText = "Server offline.";
    resultCont.classList.remove("hidden");
  } finally {
    loadingDiv.classList.add("hidden");
    btn.disabled = false;
  }
});

// 3. HELPER TO RENDER HTML
function displayResults(data) {
  resultDiv.innerHTML = ""; // Clear previous content
  resultCont.classList.remove("hidden");

  // Create a fragment to improve performance
  const fragment = document.createDocumentFragment();

  Object.entries(data).forEach(([key, value]) => {
    const row = document.createElement("div");
    row.className = "data-row";

    // Format Key: "teacher_reputation" -> "Teacher Reputation"
    const formattedKey = key.replace(/_/g, ' ');

    // Handle nested data
    let displayValue = value;
    if (typeof value === 'object' && value !== null) {
      displayValue = Array.isArray(value) ? value.join(", ") : JSON.stringify(value);
    }

    row.innerHTML = `
      <span class="data-label">${formattedKey}</span>
      <div class="data-value">${displayValue}</div>
    `;
    
    fragment.appendChild(row);
  });

  resultDiv.appendChild(fragment);
}