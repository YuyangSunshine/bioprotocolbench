# BioProtocolBench 🧪: A Benchmark for Biological Protocol Understanding and Reasoning

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/bioprotocolbench/pulls)

**The First Comprehensive Benchmark for Evaluating Biological Protocol Comprehension in AI Systems**

---

## 🌟 Overview
Biological protocols form the experimental bedrock of life science research. With the advent of high-throughput automation and AI-driven experimentation, there exists a critical need to develop models capable of **deep protocol understanding** and **experimental reasoning**. BioProtocolBench addresses this gap by providing:
- 📚 **20,000+ curated protocols** from 5 major biological protocol repositories：
  - [Protocol-exchange](https://protocolexchange.researchsquare.com/)
  - [Nature Protocols](https://www.nature.com/nprot/)
  - [Bio-protocol](https://bio-protocol.org/en)
  - [JOVE](https://www.jove.com/)
  - [MorimotoLab](https://www.morimotolab.org)
- 🎯 **5 core tasks** spanning text generation to complex reasoning：
  - Protocol Generation (GEN)
  - Protocol QA (QA)
  - Step Ordering (ORD)
  - Error Correction (ERR)
  - Experimental Reasoning (REA)
- 🧬 **16 biological subdomains** covering cutting-edge methodologies
- 🔬 **Standardized evaluation framework** for protocol-aware AI systems
  
---

## 🚀 Motivation
Biological protocols represent the **operational DNA** of experimental science. While biological research increasingly adopts automated workflows (e.g., lab robotics, AI-guided experimentation), current systems exhibit fundamental limitations:
1. **Protocol Comprehension Gap**: Existing LLMs show <40% accuracy on protocol reasoning tasks
2. **Domain Adaptation Challenge**: Biomedical LLMs fail to capture protocol-specific temporal/logical dependencies
3. **Innovation Bottleneck**: 89% of automated systems rely on fixed protocols without adaptive optimization

**Our Vision**  
Enable next-generation experimental AI systems that can:
- 🔄 **Self-optimize** experimental workflows
- 🧩 **Recombine** protocol elements for novel applications
- 🔮 **Predict** experimental outcomes from protocol descriptions

---

## 📊 Dataset Structure
### Core Components
```bash
bioprotocolbench/
├── tasks/               # Task-specific datasets
│   ├── text_generation/
│   ├── qa_multichoice/
│   ├── step_ordering/
│   ├── error_correction/
│   └── reasoning/
├── domains/             # 16 biological subdomains
├── evaluation/          # Evaluation metrics & scripts
├── protocol_db/         # Raw protocol collection
└── utils/               # Some utils files
```

---

## 🧩 Task Specifications
### 1. Protocol Generation (GEN)
- Input: Experimental objective + constraints
- Output: Valid protocol steps
- Example:
```markdown
Input: 
  Objective: Purify GFP-tagged protein from E. coli lysate
  Constraints: Use affinity chromatography, avoid expensive reagents

Output:
  1. Prepare Ni-NTA agarose beads...
  2. Centrifuge lysate at 12,000g for 15min...
```

### 2. Protocol QA (QA)
- Input: Experimental objective + constraints
- Output: Valid protocol steps
- Example:
```markdown
Input: 
  Which step ensures RNase-free conditions in RNA extraction?
  A) Ethanol precipitation  
  B) DEPC-water treatment  
  C) Phenol-chloroform extraction  
  D) Silica membrane binding

Output:
  1. Prepare Ni-NTA agarose beads...
  2. Centrifuge lysate at 12,000g for 15min...
```

### 3. Step Ordering (ORD)
- Challenge: Arrange shuffled protocol steps while maintaining experimental validity
- Evaluation Metric: Kendall's Tau (τ) with position-sensitive weighting


### 4. Error Correction (ERR)
- Task: Detect and correct protocol errors
- Error Types:
  - ❌ Thermodynamic miscalculations
  - ⚠️ Contamination risks
  - 🔀 Incubation time/temp mismatches

### 5. Experimental Reasoning (REA)
- Complex Tasks:
  - Predict downstream experimental impacts of protocol modifications
  - Recommend alternative reagents based on availability constraints
  - Optimize protocol parameters for specific experimental conditions

---

## 📈 Benchmark Results
Preliminary evaluation of state-of-the-art models:
A TABLE

---

## 💻 Getting Started

### 📦 Dataset Loading

```python
from bioprotocolbench import load_dataset

dataset = load_dataset("ProtocolGen")
print(dataset[0])
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

  - 🆕 New protocol sources
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


