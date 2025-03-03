from abc import ABC, abstractmethod
from pathlib import Path

from gpt import GPT
import time

from utility import extract_json_blocks


class Assembler(ABC):
    @abstractmethod
    def assemble(self, template_file, **kwargs):
        pass


class ConcreteAssembler(Assembler):
    def assemble(self, system_template, template_file, **kwargs):
        message = []
        # 如果存在系统设定
        if system_template:
            system_prompt = Path(system_template).read_text()
            message.append({"role": "system", "content": system_prompt})
        # 确保模板文件存在
        template = Path(template_file)
        if not template.exists():
            raise FileNotFoundError(f"Template file {template_file} not found")

        # 读取模板文件
        with open(template, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 替换模板中的占位符
        for key, value in kwargs.items():
            template_content = template_content.replace(f"{{{key}}}", str(value))

        message.append({"role": "user", "content": template_content})
        return message

class Pipeline:
    @staticmethod
    def task_one(model_file, system_promp_file, template_file, dynamic_data, check_fun, max_retries=3, sleep_time=2):
        '''
        model_file: 模型参数文件
        system_promp_file: 系统提示词文件
        template_file: 模板文件
        dynamic_data: 动态数据
        max_retries: 超时最大重试次数，默认为3次
        sleep_time: 每次重试的等待时间，默认为2秒
        return: 
            -1: 超时错误
            -2: 模型错误
            -3: 格式错误
            message: 提示词
            response_content: 回复内容
            prompt_tokens: 提示词token数
            completion_tokens: 回复token数
        '''
        # 装配提示词
        assembler = ConcreteAssembler()
        message = assembler.assemble(system_promp_file, template_file, **dynamic_data)
        # print(message)

        # 调用LLM
        llm = GPT(model_file)
        retries = 0

        while retries < max_retries:
            response = llm.query(message)
            if response == -1:
                retries += 1
                time.sleep(sleep_time) 
            elif response == -2:
                return -2
            else:
                break
        
        if response == -1:
            return -1
        
        # 处理回复
        assert isinstance(response, tuple)
        response_content, prompt_tokens, completion_tokens = response
        if 1 != check_fun(response_content):
            return -3

        return message, response_content, prompt_tokens, completion_tokens


def json_format_check(answer_text):
    json_result = extract_json_blocks(answer_text)
    if json_result:
        return 1
    return 0

# if __name__ == "__main__":
#     try:
#         # Initialize the assembler and pipeline
#         assembler = ConcreteAssembler()
#         pipeline = Pipeline()

#         # Define the template file and dynamic data
#         template_file = "./prompts/identify_one.txt"
#         dynamic_data = {
#             "file_name": "example.py",
#             "file_content": "def example():\n    pass"
#         }

#         # Define the system prompt file
#         model_file = "./model_parameters/deepseek.json"
#         system_prompt_file = "./prompts/system.txt"

#         # Run task one
#         result = pipeline.task_one(model_file, system_prompt_file, template_file, dynamic_data)
#         print("Pipeline task one result:")
#         print(result)
#     except FileNotFoundError as e:
#         print(f"File error: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
