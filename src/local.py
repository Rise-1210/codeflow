from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
class ChatModel:
    def __init__(self, model_path, tensor_parallel_size=1):
        """
        初始化模型和 tokenizer
        :param model_path: 模型路径
        :param tensor_parallel_size: GPU 并行数量，默认为 1
        """
        self.model_path = model_path
        self.tensor_parallel_size = tensor_parallel_size
        self.llm, self.tokenizer = self._load_model_and_tokenizer()

    def _load_model_and_tokenizer(self):
        """
        加载模型和 tokenizer
        """
        # 初始化 vLLM 的 LLM
        llm = LLM(model=self.model_path, max_model_len=5000,tensor_parallel_size=self.tensor_parallel_size,trust_remote_code=True)

        
        tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)

        return llm, tokenizer

    def format_chat(self, messages):
        """
        将消息列表格式化为模型所需的输入格式
        :param messages: 消息列表，格式为 [{'role': 'user', 'content': '...'}, ...]
        :return: 格式化后的 prompt
        """
        # 使用 tokenizer 的 apply_chat_template 方法自动格式化
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)
        return prompt

    def generate(self, messages, max_tokens=5000, temperature=0.6, top_p=1):
        """
        生成模型的回复
        :param messages: 消息列表，格式为 [{'role': 'user', 'content': '...'}, ...]
        :param max_tokens: 生成的最大 token 数
        :param temperature: 生成的随机性
        :param top_p: 样本概率的截断
        :return: 模型的生成结果
        """
        # 设定采样参数
        sampling_params = SamplingParams(
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )

        # 将消息列表格式化为模型所需的输入格式
        prompt = self.format_chat(messages)
        #print(prompt)

        # 进行推理
        output = self.llm.generate(prompt, sampling_params)

        # 返回生成结果
        return output
