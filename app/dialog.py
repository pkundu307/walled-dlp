
import tkinter as tk
from tkinter import ttk
import traceback


class NativeDialogUI:
    def __init__(self, root: tk.Tk, decisions):
        self.root = root
        self.decisions = decisions
        self.active_dialog = None

        # Keep a visible application window for debugging.
        self.root.title("Walled DLP - Protection Active")
        self.root.geometry("390x145")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        ttk.Label(
            root,
            text="Walled DLP is running",
            font=("Segoe UI", 13, "bold")
        ).pack(pady=(22, 8))

        ttk.Label(
            root,
            text="Monitoring ChatGPT and Perplexity"
        ).pack()

        ttk.Label(
            root,
            text="Waiting for sensitive-content requests..."
        ).pack(pady=8)

        self.root.protocol("WM_DELETE_WINDOW", self.hide)
        self.root.after(300, self.poll)

    def hide(self):
        self.root.iconify()

    def show_decision(self, item):
        print(f"[DLP UI] Showing dialog: {item.kind} - {item.label}")

        dialog = tk.Toplevel(self.root)
        self.active_dialog = dialog

        dialog.title("Walled DLP - Sensitive Content")
        dialog.geometry("460x230")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)

        ttk.Label(
            dialog,
            text="Sensitive content detected!",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(20, 10))

        description = (
            "Sensitive text prompt detected"
            if item.kind == "prompt"
            else "Sensitive file detected"
        )

        ttk.Label(
            dialog,
            text=description,
            font=("Segoe UI", 10, "bold")
        ).pack()

        ttk.Label(
            dialog,
            text=item.label,
            wraplength=420
        ).pack(pady=8)

        ttk.Label(
            dialog,
            text=item.reason,
            wraplength=420
        ).pack(pady=5)

        buttons = ttk.Frame(dialog)
        buttons.pack(pady=15)

        def finish(decision):
            print(f"[DLP UI] User selected: {decision}")

            item.decision = decision
            item.event.set()

            dialog.grab_release()
            dialog.destroy()
            self.active_dialog = None

        ttk.Button(
            buttons,
            text="Continue",
            command=lambda: finish("continue")
        ).pack(side="left", padx=15)

        ttk.Button(
            buttons,
            text="Cancel",
            command=lambda: finish("cancel")
        ).pack(side="left", padx=15)

        dialog.protocol(
            "WM_DELETE_WINDOW",
            lambda: finish("cancel")
        )

        dialog.update_idletasks()
        dialog.deiconify()
        dialog.lift()
        dialog.focus_force()
        dialog.grab_set()

    def poll(self):
        try:
            if self.active_dialog is None:
                item = self.decisions.next_nowait()

                if item:
                    self.show_decision(item)

        except Exception:
            print("[DLP UI] Dialog error:")
            traceback.print_exc()

        finally:
            self.root.after(200, self.poll)
