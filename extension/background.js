const API = "http://127.0.0.1:8765";

async function post(path, body) {
  const { apiToken } = await chrome.storage.local.get(["apiToken"]);
  if (!apiToken) throw new Error("Open the Walled DLP extension menu and save the local API token first.");
  const response = await fetch(`${API}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiToken}`
    },
    body: JSON.stringify(body)
  });
  if (!response.ok) throw new Error(`Local DLP API returned ${response.status}`);
  return response.json();
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type === "WALLED_DLP_SCAN_PROMPT") {
    post("/v1/scan/prompt", { text: message.text, page: message.page })
      .then(sendResponse).catch(error => sendResponse({ allow: false, error: error.message }));
    return true;
  }
  if (message?.type === "WALLED_DLP_SCAN_FILE") {
    post("/v1/scan/file", {
      filename: message.filename,
      mime_type: message.mimeType,
      data_base64: message.dataBase64,
      page: message.page
    }).then(sendResponse).catch(error => sendResponse({ allow: false, error: error.message }));
    return true;
  }
});
