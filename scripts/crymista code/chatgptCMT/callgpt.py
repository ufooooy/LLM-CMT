import time

import openai


def generate_response(messages, model, max_tokens=4095, temperature=0, sleep_time=25):
    """
    生成OpenAI Chat Completions响应的函数。

    :param messages: 要发送给OpenAI的消息历史记录，作为输入生成响应的基础。
    :param model: 用于生成响应的OpenAI模型的名称。
    :param max_tokens: 生成响应的最大token数限制，默认为4095。
    :param temperature: 用于控制生成文本多样性的温度参数，默认为0。
    :param sleep_time: 在发生错误时重新发送消息之前等待的时间，默认为25秒。
    :return: 生成的OpenAI响应文本。
    """

    assert messages[-1]['content'] is not None
    # 确保消息历史记录中最新一条消息的内容不为空

    # if model == 'gpt-3.5-turbo-16k' or model == 'gpt-3.5-turbo-16k-0613':
    #     # 如果使用指定的模型，则调整最大token数限制并设置OpenAI的API密钥
    #     max_tokens = 8192
    #     openai.api_key = 'define your openai key here'
    if model == 'gpt-4-turbo-preview':
        # 如果使用指定的模型，则调整最大token数限制并设置OpenAI的API密钥
        max_tokens = 4095

        openai.api_key = 'define your openai key here'

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,  # 控制文本生成的多样性
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,  # 控制对已出现词语的惩罚程度
            presence_penalty=0
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        time.sleep(sleep_time)
        # 在发生错误时，等待一段时间后重新发送消息
        return generate_response(messages, model, max_tokens)
    
    print(f'{response["usage"]["prompt_tokens"]} prompt tokens counted by the OpenAI API.')
    # 打印由OpenAI API统计的提示token数
    return response.choices[0].message['content']
