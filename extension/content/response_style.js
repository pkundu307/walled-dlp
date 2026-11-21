
(() => {
  if (window.__WALLED_DLP_RESPONSE_STYLE__) return;
  window.__WALLED_DLP_RESPONSE_STYLE__ = true;

  const style = document.createElement("style");

  style.textContent = `
    .walled-dlp-ai-response,
    .walled-dlp-ai-response * {
      color: #16803c !important;
    }

    .walled-dlp-ai-response [data-d-stream-run] {
      color: #16803c !important;
      --d-stream-ink: #16803c !important;
    }
  `;

  (document.head || document.documentElement).appendChild(style);

  function applyResponseColor() {
    const selectors = window.WALLED_DLP_SITE?.responseSelectors || [];

    for (const selector of selectors) {
      try {
        document.querySelectorAll(selector).forEach(element => {
          element.classList.add("walled-dlp-ai-response");
        });
      } catch (error) {
        console.warn("[Walled DLP] Invalid response selector:", selector);
      }
    }
  }

  let scheduled = false;

  const observer = new MutationObserver(() => {
    if (scheduled) return;

    scheduled = true;

    requestAnimationFrame(() => {
      scheduled = false;
      applyResponseColor();
    });
  });

  observer.observe(document.documentElement, {
    childList: true,
    subtree: true
  });

  applyResponseColor();

  console.log("[Walled DLP] Response color protection active.");
})();
