<h1 align="center">[ACL 2026] CodeFlowBench: A Multi-turn, Iterative
Benchmark for Complex Code Generation </h1>

<p align="center">
  <a href="https://huggingface.co/datasets/WaterWang-001/CodeFlowBench-2505">
    <img alt="Hugging Face Dataset" src="https://img.shields.io/badge/HuggingFace-CodeFlowBench-blue?logo=huggingface">
  </a>
  &nbsp;
  <a href="https://arxiv.org/abs/2504.21751">  
    <img alt="arXiv" src="https://img.shields.io/badge/arXiv-2504.21751-b31b1b?logo=arxiv">
  </a>
</p>

## 📰 News
* **[2026/04]** 🎉 Our paper has been officially accepted to the **ACL 2026 Main Conference**!

## 📖 Introduction
CodeFlowBench is a comprehensive benchmark designed to evaluate Large Language Models (LLMs) on **multi-turn**, **dependency-aware**, and **iterative** code generation tasks. Unlike traditional benchmarks that focus on single-function generation, CodeFlowBench tests a model's ability to maintain context, handle complex dependencies, and evolve code over multiple turns.

The benchmark consists of two subsets:
- **CodeFlowBench-Comp(Competitive)**: Focuses on complex competitive programming problems.
- **CodeFlowBench-Repo**: Focuses on domain-specific real-world programming problems from Github Repo.

## 📂 Directory Structure
```text
codeflowbench/
├── data/                   # Dataset files (JSON)
├── models/                 # Local model checkpoints (optional)
├── scripts/                # Bash scripts for running evaluation
├── src/                    # Source code for inference and harness
│   ├── harness.py          # Evaluation logic
│   └── utils.py            # Utility functions
├── requirements.txt        # Dependencies for All benchmark
├── requirements_repo.txt # Additional dependencies for Repo benchmark
└── README.md
```


## 🔧 Installation

First, clone the repository and set up the Conda environment:

```bash
cd codeflowbench

conda create -n codeflowbench python=3.10
conda activate codeflowbench

```

Install the dependencies:

```bash
# For CodeFlowBench All (Standard Evaluation)
pip install -r requirements.txt

# [Optional] For CodeFlowBench-Repo 
# This installs additional libraries required for executing domain-specific code
pip install -r requirements_repo.txt

```

## 📋 Preparation

### 1. Model Preparation

You can either use Hugging Face model paths directly or place your local model weights inside the `models` folder.

* **Example Path:** `models/Llama-3.1-8B-Instruct`

### 2. Data Preparation

Ensure the dataset files are located in the `./data` directory. The structure should typically contain:

* `codeflowbench_comp_test.json`
* `codeflowbench_repo.json` 

## 🏃 Quick Start

We provide convenient Bash scripts to automate the inference and evaluation process. The default scripts use `Llama-3.1-8B-Instruct` as an example.

### 🔹 CodeFlowBench-Comp

**Multi-turn Evaluation (Core):**
Evaluate the model's ability to generate code iteratively with dependencies.

```bash
bash scripts/test_multi_turn.sh

```

**Single-turn Evaluation:**
Evaluate the model in a standard single-turn setting for comparison.

```bash
bash scripts/test_single_turn.sh

```

### 🔸 CodeFlowBench-Repo

The process is similar to the  evaluation, with the following adjustments:

1. Choose `harness_repo.py` and  `codeflowbench_repo.json` in the bash script.
2. Change the import in `inference.py` to `utils_(api)_repo`.
3. Run the bash file.

## 📊 Output & Results

The evaluation logs and final scores will be saved in the `result` directory.

```
Filename Format: {model_name}_{mode}.json
Example: result/Llama-3.1-8B-Instruct_multi_turn.json
Result Content: Each entry contains the generated code, execution logs, and the pass/fail status for each turn.
```

