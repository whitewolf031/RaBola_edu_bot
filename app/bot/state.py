from typing import Dict, Any, Optional
import threading

class StateManager:
    def __init__(self):
        self._states: Dict[int, str] = {}
        self._data: Dict[int, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def set_state(self, chat_id: int, state: Optional[str]):
        with self._lock:
            if state is None:
                self._states.pop(chat_id, None)
            else:
                self._states[chat_id] = state

    def get_state(self, chat_id: int) -> Optional[str]:
        with self._lock:
            return self._states.get(chat_id)

    def set_data(self, chat_id: int, key: str, value: Any):
        with self._lock:
            if chat_id not in self._data:
                self._data[chat_id] = {}
            self._data[chat_id][key] = value

    def get_data(self, chat_id: int, key: str = None) -> Any:
        with self._lock:
            user_data = self._data.get(chat_id, {})
            if key is None:
                return user_data.copy()
            return user_data.get(key)

    def clear(self, chat_id: int):
        with self._lock:
            self._states.pop(chat_id, None)
            self._data.pop(chat_id, None)

state_manager = StateManager()

# Holatlar ro'yxati (States)
class States:
    WAITING_NAME = "WAITING_NAME"
    WAITING_PHONE = "WAITING_PHONE"
    ADMIN_WAITING_ANNOUNCEMENT = "ADMIN_WAITING_ANNOUNCEMENT"
