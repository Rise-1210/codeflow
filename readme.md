<h1 align="center"> CodeFlowBench: A Multi-turn, Iterative

Benchmark for Complex Code Generation </h1>


## 🔧 Installation

```
cd codeflowbench

conda create -n codeflowbench python=3.10
conda activate codeflowbench

pip install -r requirements.txt
```

## 📋 Preparation
For Models:
Please place your model inside the `models` folder, for example: `models/Llama-3.1-8B-Instruct`.

For Datasets:
You can use the following command to download our sampling dataset from Hugging Face.
```
wget -O data/codeflowbench_sample.json "https://huggingface.co/datasets/WaterWang-001/CodeFlowBench-2505/resolve/main/codeflowbench_sample.json"
```

## 🏃 Quick Start
You can directly use our provided Bash scripts to test the model, with only minor modifications needed (all scripts use `Llama-3.1-8B-Instruct` as an example).

* For the multi-turn coding test, use `test_multi_turn.sh`;
* For the single-turn coding test, use `test_single_turn.sh`.

## 📊 Output Statistics
The final test results will be saved in the `result` folder, with the filename format `{model_name}_{multi_turn/single_turn}.json`.




