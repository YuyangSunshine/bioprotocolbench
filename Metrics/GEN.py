import os
import json
import re
import nltk
import numpy as np
from tqdm import tqdm
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity


### Setup environment and models ###
nltk.download('punkt')
nltk.download('wordnet')

EMBEDDING_MODEL = SentenceTransformer('all-mpnet-base-v2')  # For embedding-based metrics
KEYWORD_MODEL = KeyBERT(SentenceTransformer('all-MiniLM-L6-v2')) #For keyword-based metrics

SIMILARITY_THRESHOLD = 0.7


def extract_text_response(text):
    """Extract the [ANSWER] section after stripping intermediate tags."""
    return text.split('</think>')[-1].strip().split('</Structure>')[-1].strip()\
               .split('[ANSWER_START]')[-1].strip().split('[ANSWER_END]')[0].strip()


def compute_text_generation_metrics(reference, generated):
    ref_tokens = nltk.word_tokenize(reference.lower())
    gen_tokens = nltk.word_tokenize(generated.lower())
    
    bleu = sentence_bleu([ref_tokens], gen_tokens, weights=(0.5, 0.5),
                         smoothing_function=SmoothingFunction().method1)

    meteor = meteor_score([ref_tokens], gen_tokens)

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_scores = scorer.score(reference, generated)

    return {
        "bleu": bleu,
        "meteor": meteor,
        "rouge1": rouge_scores["rouge1"].fmeasure,
        "rouge2": rouge_scores["rouge2"].fmeasure,
        "rougeL": rouge_scores["rougeL"].fmeasure
    }


def compute_keyword_overlap(ref_text, gen_text, top_k=64):
    ref_kw = set([kw for kw, _ in KEYWORD_MODEL.extract_keywords(ref_text, top_n=top_k)])
    gen_kw = set([kw for kw, _ in KEYWORD_MODEL.extract_keywords(gen_text, top_n=top_k)])
    
    if not ref_kw or not gen_kw:
        return 0.0, 0.0, 0.0

    intersection = ref_kw & gen_kw
    precision = len(intersection) / len(gen_kw)
    recall = len(intersection) / len(ref_kw)
    f1 = 2 * precision * recall / (precision + recall + 1e-8)
    return precision, recall, f1


def compute_step_recall_and_redundancy(reference_steps, generated_steps):
    ref_embeds = EMBEDDING_MODEL.encode(reference_steps)
    gen_embeds = EMBEDDING_MODEL.encode(generated_steps)

    matched_refs = set()
    matched_gens = set()

    for i, ref_vec in enumerate(ref_embeds):
        for j, gen_vec in enumerate(gen_embeds):
            if cosine_similarity([ref_vec], [gen_vec])[0][0] >= SIMILARITY_THRESHOLD:
                matched_refs.add(i)
                break

    for i, gen_vec in enumerate(gen_embeds):
        for j, ref_vec in enumerate(ref_embeds):
            if cosine_similarity([gen_vec], [ref_vec])[0][0] >= SIMILARITY_THRESHOLD:
                matched_gens.add(i)
                break

    sr = len(matched_refs) / len(reference_steps) if reference_steps else 1.0
    rp = 1.0 - ((len(generated_steps) - len(matched_gens)) / len(generated_steps)) if generated_steps else 1.0
    return sr, rp


def evaluate_protocolgen_model(result_path):
    with open(result_path, 'r') as f:
        json_list = json.load(f)

    bleu_list, meteor_list, rouge1_list, rouge2_list, rougel_list = [], [], [], [], []
    kw_precision_list, kw_recall_list, kw_f1_list = [], [], []
    sr_list, rp_list = [], []

    failed = 0

    for item in tqdm(json_list, desc="Evaluating"):
        for qa in item['QA']:
            ref = qa['output']
            gen = qa['generated_response']

            if gen is None:
                failed += 1
                continue

            gen_clean = extract_text_response(gen)

            if isinstance(ref, list):  # step-by-step protocol
                gen_steps = [step.strip() for step in gen_clean.split('\n') if step.strip()]
                sr, rp = compute_step_recall_and_redundancy(ref, gen_steps)
                sr_list.append(sr)
                rp_list.append(rp)
                ref_text = " ".join(ref)
            else:
                ref_text = str(ref)

            gen_text = str(gen_clean)
            text_metrics = compute_text_generation_metrics(ref_text, gen_text)
            bleu_list.append(text_metrics["bleu"])
            meteor_list.append(text_metrics["meteor"])
            rouge1_list.append(text_metrics["rouge1"])
            rouge2_list.append(text_metrics["rouge2"])
            rougel_list.append(text_metrics["rougeL"])

            kw_p, kw_r, kw_f1 = compute_keyword_overlap(ref_text, gen_text)
            kw_precision_list.append(kw_p)
            kw_recall_list.append(kw_r)
            kw_f1_list.append(kw_f1)

    result = {
        "BLEU": np.mean(bleu_list),
        "METEOR": np.mean(meteor_list),
        "ROUGE-1": np.mean(rouge1_list),
        "ROUGE-2": np.mean(rouge2_list),
        "ROUGE-L": np.mean(rougel_list),
        "KW_Precision": np.mean(kw_precision_list),
        "KW_Recall": np.mean(kw_recall_list),
        "KW_F1": np.mean(kw_f1_list),
        "Step_Recall": np.mean(sr_list) if sr_list else None,
        "Redundancy_Penalty": np.mean(rp_list) if rp_list else None,
        "Failed": failed / len(json_list),
        "Total": len(json_list)
    }

    return result


if __name__ == "__main__":
    output_file_path = "/absolute/path/to/LLM_output_file.json"
    print(f"Evaluating: {output_file_path}")

    results = evaluate_protocolgen_model(output_file_path)

    for key, value in results.items():
        print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")
