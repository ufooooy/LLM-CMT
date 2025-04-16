from openai import OpenAI
from llm import LLM


class GPT(LLM):
    def __init__(self, setting_file):
        super().__init__(setting_file)
        self.client = OpenAI(base_url=self.base_url, api_key=self.key)

    def check_message_format(self, message):
        assert isinstance(message, list), "message must be a list"
        assert all(isinstance(msg, dict) and "role" in msg and "content" in msg for msg in message), "message must be a list of dictionaries with 'role' and 'content' keys"

    def query(self, message):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=message,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens
        except Exception as e:
            print(f"Error: {str(e)}")
            if "timeout" in str(e).lower():
                return -1
            else:
                return -2

# if __name__ == "__main__":
#     try:
#         gpt = GPT("model_parameters/deepseek.json")
#         test_message = "你好，请你回答1+1=?"
#         response = gpt.query(test_message)
#         print("Test message:", test_message)
#         print("Response:", response)
#     except FileNotFoundError as e:
#         print(f"File error: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
