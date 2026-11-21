
(() => {
  if (window.__WALLED_DLP_RESPONSE_STYLE__) return;
  window.__WALLED_DLP_RESPONSE_STYLE__ = true;

  const style = document.createElement("style");

  style.textContent = `
    .walled-dlp-ai-response,
    .walled-dlp-ai-response * {
      color: #16803c !important;
    }
  `;

  (document.head || document.documentElement).appendChild(style);

  function applyResponseColor() {
    const selectors = [
      // ChatGPT
      '[data-message-author-role="assistant"]',
      '[data-testid^="conversation-turn-"] [data-message-author-role="assistant"]',

      // Perplexity
      'main .prose',
      'main [data-testid*="answer"]',
      'main [class*="answer"]'
    ];

    selectors.forEach(selector => {
      document.querySelectorAll(selector).forEach(element => {
        if (!element.classList.contains("walled-dlp-ai-response")) {
          element.classList.add("walled-dlp-ai-response");
        }
      });
    });
  }

  const observer = new MutationObserver(applyResponseColor);

  observer.observe(document.documentElement, {
    childList: true,
    subtree: true
  });

  applyResponseColor();

  console.log("[Walled DLP] Response color protection active.");
})();
