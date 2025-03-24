# 用到的关键包
vllm                          0.6.2+maca2.27.0.11torch2.1

torch                         2.1.2+metax2.27.0.8

transformers                  4.46.3

transformers-stream-generator 0.0.5

openai                        1.59.5
（torch/vllm无需管后缀，因为这是使用沐曦跑的；如果用api，只需要openai即可）


# 需要修改的地方
combined.py harness.py inference_api.py inference_local.py的所有输入输出地址，模型地址，base_url、api_key、Model_Name等

但基本都在代码的最前面

# 使用流程
**使用某个文件前，一定要记得修改上文所说的路径等**

## 推理
即使断开后继续推理，不会从第一个开始，而是接着上次推理的problem继续往后。

**输入路径**：codeflowbench_sample.json的路径

**输出路径**：建好的推理的输出文件夹（如output）

### 使用inference_api.py
使用的是openai接口，如需修改使用别的接口类型，请到src.api里修改

修改完路径等参数后后，直接运行即可

### 使用inference_local.py
需要使用的是下载到本地的大模型（需要修改，请到src.local里修改）

使用前需要在终端中指定使用的GPU
```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
```
并且在代码inference_local.py中修改使用的GPU数量（tensor_parallel_size）
```python
chat_model = ChatModel(model_path=MODEL_PATH,tensor_parallel_size=4)
```
然后在命令行运行即可
```bash
python inference_local.py
```

## 合并1：combined.py
**输入路径**：推理的输出文件夹（如output）

注意修改路径，默认合并的结果输出在输入路径中，名称为merged_output.json

## 运行代码并得到结果：harness.py
**输入路径**：上一步**合并1**的结果的json文件

**输出路径**：某一自己建立好的文件夹（如result）

## 合并2：combined.py
**输入路径**：运行代码结果存储的文件夹（如result）

注意修改路径，默认合并的结果输出在**输入路径**中，名称为merged_output.json