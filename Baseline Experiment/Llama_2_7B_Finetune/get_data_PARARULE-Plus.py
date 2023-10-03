import json
import random

# Load the data
with open('train.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Randomly sample 5000 entries
sampled_data = random.sample(data, 10000)

# Save the sampled data
with open('Alpaca_PARARULE-Plus.json', 'w', encoding='utf-8') as f:
    json.dump(sampled_data, f, ensure_ascii=False, indent=4)