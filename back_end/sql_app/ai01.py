from http import HTTPStatus
import dashscope

dashscope.api_key="sk-c90ade95a2b940229e0ac9f35430dc1b"
start = "续写小说："
def call_with_messages(contents:str):
    messages = [{'role': 'system', 'content': 'You are a professional novel writer.'},
                {'role': 'user', 'content': f'{start}{contents}'}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # 将返回结果格式设置为 message
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
        return response['output']['choices'][0]['message']['content']
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        return response


if __name__ == '__main__':
    response=call_with_messages("123")
    print(response)