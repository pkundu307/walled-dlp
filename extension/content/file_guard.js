(() => {
  if (window.__WALLED_DLP_FILE_GUARD__) return;
  window.__WALLED_DLP_FILE_GUARD__ = true;

  document.addEventListener("change", async (event) => {
    const input = event.target;
    if (!(input instanceof HTMLInputElement) || input.type !== "file" || !input.files?.length) return;
    if (WalledDLP.bypassFile) {
      WalledDLP.bypassFile = false;
      return;
    }
    if (WalledDLP.pendingFile) {
      event.stopImmediatePropagation();
      return;
    }

    const files = [...input.files];
    WalledDLP.pendingFile = true;
    event.stopImmediatePropagation();
    try {
      for (const file of files) {
        const result = await WalledDLP.scanFile(file);
        if (!result?.allow) {
          input.value = "";
          return;
        }
      }
      WalledDLP.bypassFile = true;
      input.dispatchEvent(new Event("change", { bubbles: true }));
    } catch (error) {
      console.error("[Walled DLP] File inspection failed; upload blocked.", error);
      input.value = "";
    } finally {
      WalledDLP.pendingFile = false;
    }
  }, true);
})();
