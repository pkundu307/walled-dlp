import threading
import uvicorn
import tkinter as tk
from app.config import HOST, PORT, API_TOKEN
from app.decision_queue import DecisionQueue
from app.dialog import NativeDialogUI
from app.logging_setup import configure_logging
from app.server import create_app

def main():
    configure_logging()
    print("Walled DLP is starting.")
    print(f"Local API: http://{HOST}:{PORT}")
    print("Extension token is stored locally in %LOCALAPPDATA%\\WalledDLP\\token.txt")
    decisions = DecisionQueue()
    api = create_app(decisions)
    config = uvicorn.Config(api, host=HOST, port=PORT, log_level="warning", access_log=False)
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    root = tk.Tk()
    NativeDialogUI(root, decisions)
    try:
        root.mainloop()
    finally:
        server.should_exit = True

if __name__ == "__main__":
    main()
