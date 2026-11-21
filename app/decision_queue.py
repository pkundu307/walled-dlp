import queue
import threading
from dataclasses import dataclass, field

@dataclass
class DecisionRequest:
    kind: str
    label: str
    reason: str
    event: threading.Event = field(default_factory=threading.Event)
    decision: str = "cancel"

class DecisionQueue:
    def __init__(self):
        self.items = queue.Queue()

    def ask(self, kind: str, label: str, reason: str, timeout: int = 180) -> str:
        item = DecisionRequest(kind=kind, label=label, reason=reason)
        self.items.put(item)
        if not item.event.wait(timeout):
            return "cancel"
        return item.decision

    def next_nowait(self):
        try:
            return self.items.get_nowait()
        except queue.Empty:
            return None
