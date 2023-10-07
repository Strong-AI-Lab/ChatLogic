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
    - `call_openai_API.py`
    - `complete_reasoning_3.5.py`
    - `complete_reasoning_4.py`
    - `complete_reasoning_Llama2.py`
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
        - `pyDatalog_processing.py`
    - **Baseline Experiment**
        - `GPT-4-1.csv`
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
