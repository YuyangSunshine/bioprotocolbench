import json
import re
import ast
from itertools import combinations
from tqdm import tqdm


def extract_predicted_order(generated_str, wrong_steps, correct_steps):
    """
    Parses the model output and reconstructs the predicted step order.

    Args:
        generated_str (str): The raw output string from the model.
        wrong_steps (List[str]): The original (shuffled) steps.
        correct_steps (List[str]): The correct step order (ground truth).

    Returns:
        Tuple[List[str], List[str]]: Predicted and correct step order.

    Raises:
        ValueError: If output is malformed or indices are invalid.
    """
    generated_str = generated_str.split("</think>")[-1]
    pattern = r"\[ANSWER_START\](.*?)\[ANSWER_END\]"
    match = re.findall(pattern, generated_str, re.DOTALL)

    if not match:
        raise ValueError("Missing [ANSWER_START]/[ANSWER_END]")

    index_str = match[-1].strip()
    try:
        generated_indices = ast.literal_eval(index_str)
    except Exception:
        raise ValueError("Cannot parse step indices as list")

    if set(generated_indices) != set(range(len(correct_steps))):
        raise ValueError("Invalid or incomplete index set")

    predicted_steps = [wrong_steps[i] for i in generated_indices]
    return predicted_steps, correct_steps


def calculate_exact_match(gts, preds):
    """
    Computes exact match accuracy between predicted and gold sequences.

    Args:
        gts (List[List[str]]): Ground truth step sequences.
        preds (List[List[str]]): Predicted step sequences.

    Returns:
        float: Exact match accuracy.
    """
    correct = sum([gt == pr for gt, pr in zip(gts, preds)])
    return correct / len(gts) if gts else 0


def calculate_kendall_tau(gts, preds):
    """
    Computes Kendall's Tau between predicted and ground truth sequences.

    Args:
        gts (List[List[str]]): Ground truth step sequences.
        preds (List[List[str]]): Predicted step sequences.

    Returns:
        float: Average Kendall's Tau score.
    """
    total_pairs = 0
    concordant_pairs = 0

    for gt, pr in zip(gts, preds):
        gt_rank = {step: i for i, step in enumerate(gt)}
        pr_rank = {step: i for i, step in enumerate(pr)}

        for a, b in combinations(gt_rank.keys(), 2):
            gt_order = gt_rank[a] - gt_rank[b]
            pr_order = pr_rank[a] - pr_rank[b]
            if gt_order * pr_order > 0:
                concordant_pairs += 1
            total_pairs += 1

    if total_pairs == 0:
        return 0
    return (2 * concordant_pairs - total_pairs) / total_pairs


def evaluate_sorting_predictions(output_file_path):
    """
    Evaluates the sorting performance of a model using a benchmark output JSON.

    Args:
        output_file_path (str): Absolute path to the JSON file.

    Returns:
        Tuple[List, List, int, int]: predicted sequences, ground truth sequences,
                                     number of failed parses, and total samples.
    """
    with open(output_file_path, 'r') as f:
        data = json.load(f)

    preds, gts = [], []
    failed, total = 0, 0

    for item in tqdm(data, desc="Evaluating"):
        for qa in item["QA"]:
            total += 1
            try:
                pr, gt = extract_predicted_order(qa["generated_response"], qa["wrong_steps"], qa["correct_steps"])
                preds.append(pr)
                gts.append(gt)
            except Exception:
                failed += 1

    return preds, gts, failed, total


def main():
    """
    Main entry point for evaluating a sorting model.
    """
    output_file_path = "/absolute/path/to/LLM_output_file.json"
    print(f"Evaluating: {output_file_path}")

    preds, gts, failed, total = evaluate_sorting_predictions(output_file_path)

    exact_match = calculate_exact_match(gts, preds)
    kendall_tau = calculate_kendall_tau(gts, preds)

    print(f"Exact Match: {exact_match:.4f}")
    print(f"Kendall's Tau: {kendall_tau:.4f}")
    print(f"Failed Parses: {failed}/{total} ({failed / total * 100:.2f}%)")
    print(f"Total Samples: {total}")
    print("---------------------------")


if __name__ == "__main__":
    main()
