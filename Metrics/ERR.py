import json
import re
from tqdm import tqdm


def extract_binary_answer(generated_str):
    """
    Extracts a binary (True/False) answer from a model-generated string.

    Args:
        generated_str (str): The raw output string from the model.

    Returns:
        bool: Parsed answer as True or False.

    Raises:
        ValueError: If parsing fails or format is invalid.
    """
    # Clean up prompt markers
    if '</think>' in generated_str:
        generated_str = generated_str.split("</think>")[-1]
    if '[/INST]' in generated_str:
        generated_str = generated_str.split("[/INST]")[-1]

    # Try to extract answer from [ANSWER_START]...[ANSWER_END]
    pattern = r"\[ANSWER_START\](.*?)\[ANSWER_END\]"
    match = re.search(pattern, generated_str, re.DOTALL)

    if match:
        answer = match.group(1).strip()
    else:
        # Fall back to last line heuristics
        generated_str = generated_str.strip()
        last_line = generated_str.split('\n')[-1]
        answer = last_line.strip()

    # Interpret answer
    if 'True' in answer or 'true' in answer:
        return True
    elif 'False' in answer or 'false' in answer:
        return False
    else:
        raise ValueError("Invalid or unrecognized answer format")


def evaluate_correction_task(output_file_path):
    """
    Evaluates model performance on the correction task benchmark.

    Args:
        output_file_path (str): Absolute path to the JSON results file.

    Returns:
        Tuple[List[bool], List[bool], int, int]: Predictions, ground truths,
                                                 number of failed parses, and total samples.
    """
    preds, gts = [], []
    failed, total = 0, 0

    with open(output_file_path, 'r') as f:
        data = json.load(f)

    for item in tqdm(data, desc="Evaluating"):
        for qa in item['Samples']:
            total += 1
            try:
                pred = extract_binary_answer(qa["generated_response"])
                gt = qa["is_correct"]
                preds.append(pred)
                gts.append(gt)
            except Exception:
                failed += 1

    return preds, gts, failed, total


def compute_classification_metrics(preds, gts):
    """
    Computes accuracy, precision, recall, and F1 score.

    Args:
        preds (List[bool]): Predicted labels.
        gts (List[bool]): Ground truth labels.

    Returns:
        dict: Dictionary with accuracy, precision, recall, and F1.
    """
    TP = sum((p is False and g is False) for p, g in zip(preds, gts))  # Correctly predicted incorrect
    FP = sum((p is False and g is True) for p, g in zip(preds, gts))   # Incorrectly flagged as incorrect
    FN = sum((p is True and g is False) for p, g in zip(preds, gts))   # Missed incorrect

    accuracy = sum(p == g for p, g in zip(preds, gts)) / len(preds) if preds else 0
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


def main():
    """
    Main entry point for evaluating a correction task result file.
    """
    output_file_path = "/absolute/path/to/LLM_output_file.json"
    print(f"Evaluating: {output_file_path}")

    preds, gts, failed, total = evaluate_correction_task(output_file_path)
    metrics = compute_classification_metrics(preds, gts)

    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1 Score: {metrics['f1']:.4f}")
    print(f"Failed Parses: {failed}/{total} ({failed / total * 100:.2f}%)")
    print(f"Total Samples: {total}")
    print('----------------------')


if __name__ == "__main__":
    main()
