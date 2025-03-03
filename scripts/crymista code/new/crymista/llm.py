from abc import abstractmethod
from pathlib import Path
import json

class LLM:
    def __init__(self, setting_file):
        if Path(setting_file).exists():
            with open(setting_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    raise ValueError(f"Setting file {setting_file} is empty")
                settings = json.loads(content)
                for key, value in settings.items():
                    setattr(self, key, value)
        else:
            raise FileNotFoundError(f"Setting file {setting_file} not found")

    @abstractmethod
    def query(message):
        pass

# if __name__ == "__main__":
#     try:
#         llm = LLM("./model_parameters/deepseek.json")
#         print("LLM settings loaded successfully.")
#         print(llm.name)
#     except (FileNotFoundError, ValueError) as e:
#         print(e)