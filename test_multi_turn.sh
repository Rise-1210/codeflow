# StepI Inference
MODEL_NAME="Llama-3.1-8B-Instruct"
MODEL_PATH="models/${MODEL_NAME}"
INPUT_FILE="data/codeflowbench_sample.json"
OUTPUT_DIR="output/${MODEL_NAME}_multi_turn_temp"

python run/multi_turn/inference_local.py \
    --model_path "${MODEL_PATH}" \
    --input_file "${INPUT_FILE}" \
    --output_dir "${OUTPUT_DIR}" \
    --tensor_parallel_size 4
## if you need to use api, you can use the follow command instead.

#MODEL_NAME="deepseek-r1"
#INPUT_PATH="data/codeflowbench_sample.json"
#OUTPUT_DIR="output/${MODEL_NAME}_multi_turn_temp"
#API_KEY="sk-XXXXX"
#API_URL="https://xxxxx.com/v1"

#python  run/multi_turn/inference_api.py \
#  --model_name "$MODEL_NAME" \
#  --input_file "$INPUT_PATH" \
#  --output_dir "$OUTPUT_DIR" \
#  --api_key "$API_KEY" \
#  --api_url "$API_URL"

python run/multi_turn/combined.py\
    --model_name "${MODEL_NAME}" \
    --combined_dir "${OUTPUT_DIR}"


# StepII Harness
MODEL_NAME="Llama-3.1-8B-Instruct"
INPUT_PATH="output/inference/${MODEL_NAME}_multi_turn.json"
OUTPUT_DIR="output/${MODEL_NAME}_multi_turn_temp"

python run/multi_turn/harness.py \
  --input_path "$INPUT_PATH" \
  --output_dir "$OUTPUT_DIR" \
  --model_name "$MODEL_NAME"


python run/multi_turn/combined.py\
    --model_name "${MODEL_NAME}" \
    --combined_dir "${OUTPUT_DIR}"\
    --harness

# StepIII Stat
python run/multi_turn/stat.py\
    --input "output/harness/${MODEL_NAME}_multi_turn.json"\
    --output "result/${MODEL_NAME}_multi_turn.json"


