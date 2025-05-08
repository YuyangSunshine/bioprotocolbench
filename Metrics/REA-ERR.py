import json
import re
from tqdm import tqdm


def extract_binary_answer(generated_str):
    """Extract True/False answer from generated string."""
    if '</think>' in generated_str:
        generated_str = generated_str.split("</think>")[-1]

    pattern = r"\[ANSWER_START\](.*?)\[ANSWER_END\]"
    match = re.search(pattern, generated_str, re.DOTALL)
    if match:
        answer = match.group(1).strip()
    else:
        answer = generated_str.strip().split('\n')[-1]

    if 'True' in answer or 'true' in answer:
        return True
    elif 'False' in answer or 'false' in answer:
        return False
    else:
        raise ValueError("Invalid or unrecognized answer format.")


def evaluate_step_reasoning_model(result_path):
    llm_judge = 0
    total = 0
    failed = 0

    with open(result_path, 'r') as f:
        data = json.load(f)

    for item in tqdm(data, desc="Evaluating Step Reasoning"):
        for qa in item['QA']:
            if "LLM_judge" in qa:
                total += 1
                try:
                    is_correct = extract_binary_answer(qa['LLM_judge'])
                    llm_judge += int(is_correct)
                except Exception:
                    failed += 1
                    continue

    acc = llm_judge / (total - failed) * 100 if (total - failed) > 0 else 0
    fail_rate = failed / total * 100 if total > 0 else 0

    return {
        "Consistency": acc,
        "Failure_Rate": fail_rate,
        "Total": total,
        "Failed": failed,
    }


if __name__ == "__main__":
    """
    Main entry point for evaluating a Reasoning for Error Correction task result file.
    """
    output_file_path = "/absolute/path/to/LLM_output_file.json"
    print(f"Evaluating: {output_file_path}")
    results = evaluate_step_reasoning_model(output_file_path)
    print(f"LLM_judge: {results['LLM_Judge_Accuracy']:.2f}%")
    print(f"Failed: {results['Failure_Rate']:.2f}%")
    print(f"Total: {results['Total']}")
    print('----------------------')
