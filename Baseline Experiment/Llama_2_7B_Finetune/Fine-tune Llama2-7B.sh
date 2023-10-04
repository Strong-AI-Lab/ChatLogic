ssh https://github.com/tloen/alpaca-lora.git
# put the data "./Alpaca_PARARULE-Plus.json" into the directory same as the github repo
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