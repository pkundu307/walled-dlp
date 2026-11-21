const input = document.getElementById("token");
const status = document.getElementById("status");

chrome.storage.local.get(["apiToken"]).then(({apiToken}) => {
  if (apiToken) status.textContent = "A local API token is already saved.";
});

document.getElementById("save").addEventListener("click", async () => {
  const token = input.value.trim();
  if (!token) {
    status.textContent = "Enter the token first.";
    return;
  }
  await chrome.storage.local.set({apiToken: token});
  input.value = "";
  status.textContent = "Token saved in this browser profile.";
});
