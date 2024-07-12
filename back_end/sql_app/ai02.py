from http import HTTPStatus
import dashscope

dashscope.api_key="sk-c90ade95a2b940229e0ac9f35430dc1b"

def call_with_messages(question:str, context:str):
    template_system = """
    现在需要你阅读一篇文章并回答问题。请阅读以下文章并回答问题。如果你不知道答案，请回答“我不知道”。请简要的回答问题，不需要写太多内容。
    """
    template_user = """
    现在需要你阅读一篇文章并回答问题。请阅读以下文章并回答问题。如果你不知道答案，请回答“我不知道”。
    问题: {question} 
    文章: {context} 
    """
    filled_template_user = template_user.format(question=question, context=context)
    messages = [{'role': 'system', 'content': 'You are a professional assistant.'},
                {'role': 'user', 'content': filled_template_user}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # 将返回结果格式设置为 message
    )
    if response.status_code == HTTPStatus.OK:
        # print(response)
        return response['output']['choices'][0]['message']['content']
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        return response


if __name__ == '__main__':
    response=call_with_messages("父亲干了哪些事情")
    print(response)