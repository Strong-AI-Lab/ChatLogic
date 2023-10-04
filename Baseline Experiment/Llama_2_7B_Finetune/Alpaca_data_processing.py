from datasets import load_dataset
import json

def transform_data(original_data):
    # fixed value of instruction
    instruction_text = """Based on the closed world assumption, please help me complete a multi-step logical reasoning task (judge true or not). Please help me answer whether the question is correct or not based on the facts and rules formed by these natural language propositions. You should just return me one number as the final answer (1 for true and 0 for wrong) without providing any reasoning process. The input contains all propositions, each sentence is an independent proposition, and the question, and the output is the answer to the question."""

    # Transform data
    transformed_data = []
    for entry in original_data:
        new_entry = {
            "instruction": instruction_text,
            "input": f"Propositions: {entry['context']}, Question: {entry['question']}",
            "output": entry['label']
        }
        transformed_data.append(new_entry)

    return transformed_data

def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    # load data
    dataset = load_dataset("qbao775/PARARULE-Plus")


    # Convert each data slice and save it separately
    for split, filename in zip(["train", "validation", "test"], ["train.json", "val.json", "test.json"]):
        # Slice the dataset
        data_slice = dataset[split]
        transformed_data = transform_data(list(data_slice))
        save_to_json(transformed_data, filename)
        print(f"Transformed and saved {split} data to {filename}.")

if __name__ == "__main__":
    main()