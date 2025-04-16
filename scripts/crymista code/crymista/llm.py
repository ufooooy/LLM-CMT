from abc import ABC, abstractmethod
from pathlib import Path
import json

class LLM(ABC):
    def __init__(self, setting_file):
        self.load_settings(setting_file)

    def load_settings(self, setting_file):
        if not Path(setting_file).exists():
            raise FileNotFoundError(f"Setting file {setting_file} not found")
        
        with open(setting_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                raise ValueError(f"Setting file {setting_file} is empty")
            settings = json.loads(content)
            for key, value in settings.items():
                setattr(self, key, value)

    @abstractmethod
    def query(self, message):
        pass