# ChatLogic

ChatLogic is a method that uses symbolic reasoning engines to augment the reasoning capabilities of large language models.

Before you start implementing this project, please follow the basic design process below.

## Installation

```shell
conda create -n ChatLogic python=3.10
conda activate ChatLogic
git clone https://github.com/Strong-AI-Lab/ChatLogic.git
cd ChatLogic
pip install -r requirements.txt
```

## File Structure

- **ChatLogic**
    - `call_openai_API.py`  # Call OPENAI’s GPT API
    - `complete_reasoning_3.5.py`  # Complete the reasoning test fot GPT-3.5
    - `complete_reasoning_4.py`  # Complete the reasoning test fot GPT-34
    - `complete_reasoning_Llama2.py` # Complete the reasoning test fot Llama2 7B
    - `cwa_processing_animal.py`
    - `cwa_processing_people.py`
    - `PARARULE_Plus.py`
    - `pyDatalog_processing.py`
    - `README.md`
    - `requirements.txt`
    - `sample_extraction.py`
    - `templates.py`
    - **Ablation Study**
        - `Ablation_study_gpt3.5.py`
        - `Ablation_study_gpt4.py`
        - `Ablation_study_Llama2.py`
    - **Baseline Experiment**
        - `GPT3.5.py`
        - `GPT4.py`
        - `Llama2.py`
        - **Llama_2_7B_Finetune**
            - `Alpaca_data_processing.py`
            - `Fine-tune Llama2-7B.sh`
            - `get_data_PARARULE-Plus.py`
            - `prompt_processing.py`
            - `test_Llama2-7B_finetune.py`
        - **Zero-shot CoT**
            - `GPT-3.5.py`
            - `GPT-4.py`
            - `Llama 2-7B.py`


## Use LoRA to finetune Llama-2 7B

We use Stanford Alpaca paradigm to train the fine-tuned Llama2 model, you can see the specific operating specifications [here](https://github.com/tloen/alpaca-lora).

The data set adjusted for Alpaca format is already visible on Huggingface [("ZhongshengWang/PARARULE-Plus-Alpaca")](https://huggingface.co/datasets/ZhongshengWang/PARARULE-Plus-Alpaca).

Using the NVIDIA RTX3090 graphics card, the effect after 5h LoRA fine-tuning on 10,000 pieces of data (randomly extracted) is significantly improved compared to the native model.

Just create a random selected data (10,000 pieces) and save it to the file called "Alpaca_PARARULE-Plus.json" which in the same location of the git repo.

Shell command below. But you can also tweak our hyperparameters:


```shell
clone https://github.com/tloen/alpaca-lora.git

python finetune.py \
    --base_model 'meta-llama/Llama-2-7b-hf' \
    --data_path './Alpaca_PARARULE-Plus.json' \
    --output_dir './lora-alpaca' \
    --batch_size 128 \
    --micro_batch_size 4 \
    --num_epochs 5 \
    --learning_rate 1e-4 \
    --cutoff_len 512 \
    --val_set_size 2000 \
    --lora_r 8 \
    --lora_alpha 16 \
    --lora_dropout 0.05 \
    --lora_target_modules '[q_proj,v_proj]' \
    --train_on_inputs \
    --group_by_length
```
## Quick Start

Before you start the reasoning using ChatGPT/GPT-4 set the global param in the environment configuration **OPENAI_API_KEY="your_api_key"**