import json
from typing import Any, Dict

from state.StorageAbc import BaseStorage


class FileStorage(BaseStorage):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(state, file)

    def retrieve_state(self) -> Dict[str, Any]:
        try:
            dict_state = dict()
            with open(self.file_path, 'r') as file:
                for line in file:
                    dict_state.update(json.loads(line))
            return dict_state
        except IOError:
            return dict()
        except json.JSONDecodeError:
            return dict()
        except FileNotFoundError:
            return dict()
