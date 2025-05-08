import json
import re
from tqdm import tqdm
import numpy as np
from sklearn.metrics import brier_score_loss

def extract_answer_and_confidence(generated_str):
    """
    Extracts the answer and confidence score from a generated string.

    Expected format in the string:
        [ANSWER_START] ... [ANSWER_END] with confidence (as number)

    Returns:
        tuple: (answer: str, confidence: int)

    Raises:
        ValueError: if parsing fails or confidence is invalid.
    """
    # Remove intermediate thinking steps if present
    if '</think>' in generated_str:
        generated_str = generated_str.split("</think>")[-1]

    # Extract content between [ANSWER_START] and [ANSWER_END]
    pattern = r"\[ANSWER_START\](.*?)\[ANSWER_END\]"
    match = re.search(pattern, generated_str, re.DOTALL)
    if not match:
        raise ValueError("Missing [ANSWER_START] or [ANSWER_END]")

    content = match.group(1).strip()

    # Handle possible answer-confidence formats
    if '&' in content:
        parts = content.split('&')
        if len(parts) != 2:
            raise ValueError("Expected one '&' to separate answer and confidence")
    else:
        parts = content.split(' ')
        parts = [' '.join(parts[:-1]), parts[-1]]

    answer = parts[0].strip()

    # Extract numerical confidence
    confidence_match = re.search(r"\d+", parts[-1])
    if not confidence_match:
        raise ValueError("Confidence value not found")
    confidence = int(confidence_match.group())

    if confidence > 100:
        raise ValueError("Confidence cannot exceed 100")

    return answer, confidence


def evaluate_predictions(output_file_path):
    """
    Evaluates predictions from a JSON output file.

    Args:
        output_file_path (str): Absolute path to the JSON file containing model outputs.

    Returns:
        tuple:
            accs (List[int]): List of binary accuracy values.
            cfds (List[int]): List of confidence scores.
            failed (int): Number of failed parses.
            total (int): Total number of examples processed.
    """
    with open(output_file_path, 'r') as f:
        data = json.load(f)

    accs = []
    cfds = []
    failed = 0
    total = 0

    for item in tqdm(data, desc="Evaluating"):
        for qa in item['Samples']:
            total += 1
            generated_str = qa['generated_response']
            try:
                answer, confidence = extract_answer_and_confidence(generated_str)
                cfds.append(confidence)
                accs.append(1 if answer == qa['answer'] else 0)
            except Exception:
                failed += 1

    return accs, cfds, failed, total


def main():
    """
    Entry point for evaluation. Define the absolute path to the output JSON file here.
    """
    output_file_path = "/absolute/path/to/LLM_output_file.json"
    print(f"Evaluating: {output_file_path}")

    accs, cfds, failed, total = evaluate_predictions(output_file_path)

    accuracy = sum(accs) / len(accs) if accs else 0
    brier = brier_score_loss(accs, np.array(cfds) / 100) if accs else None

    print(f'Failed parses: {failed}/{total} ({failed / total * 100:.2f}%)')
    print(f'Total samples: {total}')
    print(f'Accuracy: {accuracy:.4f}')
    if brier is not None:
        print(f'Brier Score: {brier:.4f}')
    print('-----------------------')


if __name__ == "__main__":
    main()
