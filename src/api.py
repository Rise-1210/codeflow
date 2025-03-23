import openai
class ChatModelAPI:
    def __init__(self, api_url, api_key,model_name):
        """
        初始化 API 连接
        :param api_url: API 的地址
        :param api_key: 可选的 API Key，用于身份验证
        """
        self.api_url = api_url
        self.api_key = api_key
        self.model_name = model_name


    def generate(self, messages, max_tokens=512, temperature=0.6, top_p=1):
        client = openai.OpenAI(api_key=self.api_key,base_url=self.api_url)
        response = client.chat.completions.create(
        model=self.model_name,
        messages=[{"role": "user", "content": messages}],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=0
    )
    
        return response


