import threading
from app.decision_queue import DecisionQueue

def test_decision_queue_returns_cancel_on_timeout():
    queue = DecisionQueue()
    assert queue.ask("prompt", "test", "reason", timeout=0) == "cancel"
