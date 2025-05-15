import requests
import openai
class ChatModelAPI:
    def __init__(self, api_url, api_key,model_name):
        """
        Initialize API connection
        :param api_url: API URL
        :param api_key: Optional API Key for authentication
        """
        self.api_url = api_url
        self.api_key = api_key
        self.model_name = model_name


    def generate(self, messages, max_tokens=4000, temperature=0.6, top_p=1):
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


