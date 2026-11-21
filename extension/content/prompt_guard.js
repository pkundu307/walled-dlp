
(() => {
  if (window.__WALLED_DLP_PROMPT_GUARD__) return;
  window.__WALLED_DLP_PROMPT_GUARD__ = true;

  let checking = false;
  let bypass = false;

  function getComposer(eventTarget) {
    if (eventTarget instanceof Element &&
        eventTarget.matches('textarea,[contenteditable="true"],[role="textbox"]')) {
      return eventTarget;
    }

    return document.querySelector(
      'textarea, [contenteditable="true"], [role="textbox"]'
    );
  }

  function getText(el) {
    return el?.value ?? el?.innerText ?? el?.textContent ?? "";
  }

  function getSubmitButton(composer) {
    const form = composer?.closest("form");
    if (!form) return null;

    return form.querySelector(
      'button[type="submit"], button[aria-label*="Send" i], button[data-testid*="send" i]'
    );
  }

  async function inspectPrompt(event, composer, action) {
    if (bypass) {
      bypass = false;
      return;
    }

    if (checking) {
      event.preventDefault();
      event.stopImmediatePropagation();
      return;
    }

    const text = getText(composer).trim();
    if (!text) return;

    checking = true;
    event.preventDefault();
    event.stopImmediatePropagation();

    try {
      console.log("[Walled DLP] Inspecting prompt...");

      const result = await WalledDLP.scanPrompt(text);

      console.log("[Walled DLP] Scan result:", result);

      if (!result || result.allow !== true) {
        console.warn("[Walled DLP] Submission blocked.");
        return;
      }

      bypass = true;
      action();

    } catch (error) {
      console.error("[Walled DLP] Inspection failed:", error);
    } finally {
      checking = false;
    }
  }

  // Handle Enter key
  document.addEventListener("keydown", event => {
    if (event.key !== "Enter" ||
        event.shiftKey ||
        event.isComposing) return;

    const composer = getComposer(event.target);
    if (!composer) return;

    inspectPrompt(event, composer, () => {
      const form = composer.closest("form");

      if (form) {
        form.requestSubmit();
      } else {
        const button = getSubmitButton(composer);
        if (button) button.click();
        else console.error("[Walled DLP] Submit button not found.");
      }
    });
  }, true);

  // Handle Send button
  document.addEventListener("click", event => {
    const button = event.target instanceof Element
      ? event.target.closest("button")
      : null;

    if (!button) return;

    const label = [
      button.getAttribute("aria-label"),
      button.getAttribute("data-testid"),
      button.innerText
    ].join(" ").toLowerCase();

    if (!/send|submit|ask|search/.test(label)) return;

    const composer = getComposer(document.activeElement)
      || document.querySelector('textarea,[contenteditable="true"],[role="textbox"]');

    if (!composer) return;

    inspectPrompt(event, composer, () => button.click());

  }, true);

})();
