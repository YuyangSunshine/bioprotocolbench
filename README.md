![logo-v2](https://github.com/user-attachments/assets/252d8212-722b-46ec-97b9-b72f4ae3c4bf)


# BioProBench: A Comprehensive Dataset and Benchmark for LLMs in Biological Protocol Understanding and Reasoning

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/bioprotocolbench/pulls)

**To our knowledge, BioProBench is the first large-scale, integrated multi-task benchmark for biological protocol understanding and reasoning, encompassing not only question answering but also step ordering, error correction, protocol generation and structured reasoning.**

---

## 🌟 Overview
Biological protocols form the experimental bedrock of life science research. With the advent of high-throughput automation and AI-driven experimentation, there exists a critical need to develop models capable of **deep protocol understanding** and **experimental reasoning**. BioProtocolBench addresses this gap by providing:
- 📚 **27K curated protocols** from 6 major biological protocol repositories：
  - [Protocol.io](https://www.protocols.io/)
  - [Protocol-exchange](https://protocolexchange.researchsquare.com/)
  - [Nature Protocols](https://www.nature.com/nprot/)
  - [Bio-protocol](https://bio-protocol.org/en)
  - [JOVE](https://www.jove.com/)
  - [MorimotoLab](https://www.morimotolab.org)
- 🎯 **5 core tasks** spanning text generation to complex reasoning：
  - Protocol QA (QA)
  - Step Ordering (ORD)
  - Error Correction (ERR)
  - Protocol Generation (GEN)
  - Experimental Reasoning (REA)
- 🧬 **16 biological subdomains** covering cutting-edge methodologies
- 🔬 **Standardized evaluation framework** for protocol-aware AI systems
  
---

## 🚀 Motivation
Biological protocols represent the **operational DNA** of experimental science. While biological research increasingly adopts automated workflows (e.g., lab robotics, AI-guided experimentation), current systems exhibit fundamental limitations:
1. **Protocol Comprehension Gap**: Existing LLMs show <40% accuracy on protocol reasoning tasks
2. **Domain Adaptation Challenge**: Biomedical LLMs fail to capture protocol-specific temporal/logical dependencies
3. **Innovation Bottleneck**: 89% of automated systems rely on fixed protocols without adaptive optimization

---

## 📊 Dataset Structure
### Core Components
```bash
bioprotocolbench/
├── Metrics/               # Evaluation metrics & scripts
│   ├── text_generation/
│   ├── qa_multichoice/
│   ├── step_ordering/
│   ├── error_correction/
│   └── reasoning/
└── readme              
```

---

### 🧪 Evaluation Metrics

Each task in **BioProtocolBench** includes a standalone evaluation script. To evaluate your model outputs:

#### ✅ Step 1: Locate the evaluation file

Each task corresponds to one script:

| Task                         | Script       | Metrics     |
| ---------------------------- | ------------ |------------ |
| Protocol Generation (GEN)    | `GEN.py`     |BLEU, Keyword-based, Embedding-based, etc. |
| Protocol QA (PQA)            | `PQA.py`     |Accuracy, Brier Score, etc. |
| Error Correction (ERR)       | `ERR.py`     |Accuracy, Precision, Recall, F1, etc. |
| Step Ordering (ORD)          | `ORD.py`     |Exact Match, Kendall's tau, etc. |
| Experimental Reasoning (REA) | `REA-ERR.py` |Accuracy, Precision, Recall, F1, Consistency, etc. |


#### ✏️ Step 2: Modify the script

Open the corresponding evaluation script (e.g., `ERR.py`) and **manually set** the file path to your model’s output JSON file:

```python
# Inside ERR.py

def main():
    output_file_path = "/absolute/path/to/LLM_output_file.json"  # ← Replace this!
    ...
```

Example:

```python
output_file_path = "./ErrorCorrection_Benchmark_gpt-4o.json"
```

Then run the script:

```bash
python ERR.py
```


#### 🧪 Output Metrics

Each script prints evaluation results such as:

* Accuracy, Precision, Recall, F1
* Step-level metrics (e.g., Step Recall, Redundancy Penalty)
* Ordering metrics (e.g., Kendall’s Tau)
* Parsing failure rates

---

## 🤝 Contributing
- We welcome contributions through:

  - New protocol sources
  - 🧪 Additional biological domains
  - 🧠 Novel evaluation tasks
  - 📝 Annotation improvements

---

## 📜 Citation
```bibtex
@misc{bioprotocolbench2025,
  title={BioProtocolBench: A Benchmark for Biological Protocol Understanding and Reasoning},
  author={Name et al.},
  year={2025},
  url={https://github.com/YuyangSunshine/bioprotocolbench/}
}
```

---

## 📧 Contact
For dataset access or collaboration inquiries:
sunshineliuyuyang@gmail.com


