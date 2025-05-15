from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
class ChatModel:
    def __init__(self, model_path, tensor_parallel_size=1):
        """
        Initialize the model and tokenizer
        :param model_path: model path
        :param tensor_parallel_size: GPU parallel number, default is 1
        """
        self.model_path = model_path
        self.tensor_parallel_size = tensor_parallel_size
        self.llm, self.tokenizer = self._load_model_and_tokenizer()

    def _load_model_and_tokenizer(self):
        """
        Loading the model and tokenizer
        """
        # Initialize the vLLM's LLM
        llm = LLM(model=self.model_path, max_model_len=5120,tensor_parallel_size=self.tensor_parallel_size,trust_remote_code=True,gpu_memory_utilization=0.8)

        
        tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)

        return llm, tokenizer

    def format_chat(self, messages):
        """
        Format the message list into the input format required by the model
        :param messages: message list, format is [{'role': 'user', 'content': '...'}, ...]
        :return: formatted prompt
        """
        # 使用 tokenizer 的 apply_chat_template 方法自动格式化
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)
        return prompt

    def generate(self, messages, max_tokens=10000, temperature=0.6, top_p=1):
        """
        Generate model responses
        :param messages: message list, format is [{'role': 'user', 'content': '...'}, ...]
        :param max_tokens: maximum number of tokens generated
        :param temperature: randomness of generation
        :param top_p: sample probability cutoff
        :return: model generation results
        """
        # Set sampling parameters
        sampling_params = SamplingParams(
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )

        # Format the message list into the input format required by the model
        prompt = self.format_chat(messages)
        #print(prompt)

        # Making inferences
        output = self.llm.generate(prompt, sampling_params)

        # Returns the generated result
        return output

