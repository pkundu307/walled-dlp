(() => {
  if (window.__WALLED_DLP_COMMON__) return;
  window.__WALLED_DLP_COMMON__ = true;

  window.WalledDLP = {
    page: location.hostname,
    bypassPrompt: false,
    bypassFile: false,
    pendingPrompt: false,
    pendingFile: false,
    async scanPrompt(text) {
      return chrome.runtime.sendMessage({
        type: "WALLED_DLP_SCAN_PROMPT",
        text,
        page: location.hostname
      });
    },
    async scanFile(file) {
      const buffer = await file.arrayBuffer();
      const bytes = new Uint8Array(buffer);
      let binary = "";
      const chunk = 0x8000;
      for (let i = 0; i < bytes.length; i += chunk) {
        binary += String.fromCharCode(...bytes.subarray(i, i + chunk));
      }
      return chrome.runtime.sendMessage({
        type: "WALLED_DLP_SCAN_FILE",
        filename: file.name,
        mimeType: file.type || "application/octet-stream",
        dataBase64: btoa(binary),
        page: location.hostname
      });
    },
    getComposerText() {
      const selectors = [
        'textarea',
        '[contenteditable="true"]',
        '[role="textbox"]'
      ];
      const elements = selectors.flatMap(s => [...document.querySelectorAll(s)]);
      const visible = elements.filter(el => el.getClientRects().length);
      const el = visible.sort((a, b) => (b.innerText || b.value || "").length - (a.innerText || a.value || "").length)[0];
      return el ? (el.value ?? el.innerText ?? el.textContent ?? "") : "";
    }
  };
})();
