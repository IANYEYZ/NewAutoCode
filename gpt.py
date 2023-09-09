import openai
class chatgpt:
    '基本的与chatGPT通信的代码封装'
    apikey = ""
    message = []

    def set_api_key(self,api_key):
        self.apikey = api_key
        openai.api_key = self.apikey
    
    def clear_message(self):
        self.message = []
    
    def get_response(self,prompt,role = 'user',model_ = 'gpt-3.5-turbo-16k',temperature_ = 0):
        self.message.append({'role': role, 'content': prompt})
        response = openai.ChatCompletion.create(
            model=model_,
            messages=self.message,
            temperature=temperature_,
            stream=True  # again, we set stream=True
        )
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta']
            chunk_message = chunk_message.get('content','')
            yield chunk_message
    
    def add_message(self,prompt,role = 'assistant'):
        self.message.append({'role': role, 'content': prompt})