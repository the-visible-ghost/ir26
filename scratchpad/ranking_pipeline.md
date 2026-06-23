
# Master Filtering Pipeline ->

> - ### take a ranking of suspiciousness and map it to all candidates, increment if they fail the checks listed below.
> - ![>](https://img.shields.io/badge/TODO-blue) {add additional checks defn}

- ## Sanity + Honeypot Detection [(to edit)]
  - don't care about the candidate, just make sure the profile is realistically valid and internally consistent.
  - ###Checks--
      - Experience vs Career History
        > match the total career jobs duration with the claimed experience
        
      - Claimed Proficiency vs actual career duration
        > if a candidate claims to be `expert` in `python`, but his career duration is unrealistic like under 5 or 0, then he fails this test.
      
      - `len(expert_languages)` > `years_of_exp`^2
      
      - career jobs timeline overlap [Special Case]
        > candidate worked `2023-2024` in Google and `2021-2025` in Flipkart, which overlaps with Google.
          this doesn't directly increase the suspiciousness because it can be possible in some cases.
          This is a special case that alters/checks/calls these additional checks: ![>](https://img.shields.io/badge/TODO-blue)

- ## Archetype Classification
    > - get what kind of engineer the candidate is and prepare the specific filters and keywords based on it.
    > - instead of filtering with keywords, use their archetype and past works to analyze [ex4](#example-4)


# Examples
- ## Example 4

- # UNCHECKED BELOW

## High-Level Architecture

The system consists of two phases:

```text
PRE-PROCESSING (Offline)
    ↓
Build Candidate Knowledge Base
    ↓
Build Multi-Vector Indexes

RUNTIME
    ↓
Process JD
    ↓
Retrieve Candidates
    ↓
Aggregate Scores
    ↓
Apply Behavioral Layer
    ↓
Final Ranking
    ↓
Honeypot Audit
```

---

# PHASE 1 — PRE-PROCESSING (OFFLINE)

Executed once.

Purpose:

```text
100,000 raw candidates
        ↓
structured semantic representations
        ↓
candidate embeddings
        ↓
search indexes
```

No JD is involved yet.

---

# Stage 1 — Candidate Understanding

## Input

Raw candidate object.

Example:

```json
{
  "headline": "Senior ML Engineer",
  "years_of_experience": 7,
  "career_history": [
    {
      "title": "ML Engineer",
      "description": "Built recommendation systems..."
    }
  ],
  "skills": [
    {"name": "FAISS"},
    {"name": "Embeddings"},
    {"name": "Python"}
  ]
}
```

---

## Goal

Convert noisy profile information into structured semantic evidence.

Instead of storing:

```text
FAISS
Embeddings
Python
```

we want:

```text
Candidate has:
- Retrieval experience
- Production ML experience
- Search infrastructure experience
- Recommendation systems experience
```

---

## Output

Candidate Evidence Object

```python
CandidateEvidence(
    seniority="Senior",

    domains=[
        "Retrieval",
        "Ranking",
        "Recommendations"
    ],

    industries=[
        "Software"
    ],

    career_signals=[
        "Product Company",
        "Production ML"
    ]
)
```

This evidence object is passed to the next stage.

---

# Stage 2 — Skill Clustering

Consumes:

```python
CandidateEvidence
```

plus raw skills.

---

## Input

```python
skills = [
    "FAISS",
    "Qdrant",
    "Embeddings",
    "Python",
    "LoRA"
]
```

---

## Processing

Map individual skills into semantic clusters.

Example:

```text
FAISS
Qdrant
Embeddings
```

↓

```text
Retrieval Systems
```

---

```text
LoRA
PEFT
QLoRA
```

↓

```text
LLM Fine-Tuning
```

---

## Output

```python
SkillClusterObject(
    clusters=[
        "Retrieval Systems",
        "LLM Fine-Tuning"
    ],

    evidence={
        "Retrieval Systems":
        [
            "FAISS",
            "Qdrant",
            "Embeddings"
        ],

        "LLM Fine-Tuning":
        [
            "LoRA"
        ]
    }
)
```

Notice:

We preserve evidence.

This is important later for explanations.

---

# Stage 3 — Career Intelligence Extraction

Consumes:

```python
career_history
```

---

## Input

```text
ML Engineer
Built recommendation system

Senior AI Engineer
Built vector search platform

Lead ML Engineer
Owned ranking infra
```

---

## Processing

Infer latent career signals.

Not keywords.

Meaning.

---

Example:

```text
Built recommendation systems
```

↓

```text
Recommendation Experience
```

---

```text
Owned vector search platform
```

↓

```text
Retrieval Experience
```

---

```text
Deployed to production
```

↓

```text
Production ML
```

---

## Output

```python
CareerIntelligence(
    seniority="Senior",

    experience_years=7,

    inferred_capabilities=[
        "Retrieval",
        "Ranking",
        "Recommendations",
        "Production ML"
    ],

    evidence={
        "Retrieval":
        [
            "Built vector search platform"
        ],

        "Ranking":
        [
            "Owned ranking infra"
        ]
    }
)
```

---

# Stage 4 — Candidate Semantic Representation Generation

Consumes:

```python
CandidateEvidence
SkillClusterObject
CareerIntelligence
Raw Profile
```

Now we generate the actual embedding texts.

---

## Vector A — Identity

### Input

```python
headline
summary
title
industry
experience
```

---

### Generated Text

```text
Senior AI Engineer with 7 years of experience
working in product companies building AI systems.
```

---

## Vector B — Career

### Input

```python
CareerIntelligence
```

---

### Generated Text

```text
Built recommendation systems,
retrieval systems,
ranking systems,
production ML infrastructure.
```

---

## Vector C — AI Expertise

### Input

```python
CareerIntelligence
SkillClusterObject
```

---

### Generated Text

```text
Experience with embeddings,
retrieval systems,
vector databases,
LLM fine tuning.
```

---

## Vector D — Systems

Generated from:

```python
backend
distributed systems
cloud
infra
```

---

## Vector E — Skills

Generated from:

```python
SkillClusterObject
```

Example:

```text
Retrieval Systems:
FAISS
Qdrant
Embeddings

LLM Fine-Tuning:
LoRA
```

---

## Vector F — Validation

Generated from:

```python
education
certifications
github
```

---

## Vector G — Recruitability

Generated from:

```python
location
notice period
work mode
relocation
```

---

# Stage 5 — Candidate Index Creation

Consumes:

```python
7 candidate vectors
```

---

## Embedding

Each vector:

```python
text
    ↓
embedding model
    ↓
768 dimensional vector
```

---

Example

```python
career_text
    ↓
embedding
    ↓
[0.12, 0.87, ...]
```

---

## Index Storage

Separate index per semantic aspect.

```python
index_identity
index_career
index_ai
index_system
index_skill
index_validation
index_recruitability
```

Stored:

```python
candidate_id
embedding
```

---

Preprocessing ends here.

---

# PHASE 2 — RUNTIME

Begins when a JD arrives.

---

# Stage 6 — JD Understanding

## Input

Raw JD text.

---

## Processing

Decompose JD into semantic requirements.

---

Example

JD says:

```text
Production experience with embeddings-based retrieval systems
```

Extract:

```python
Capability:
    Retrieval

Evidence:
    Embeddings
    Vector Search
```

---

JD says:

```text
Experience designing evaluation frameworks
```

Extract:

```python
Capability:
    Ranking Evaluation
```

---

## Output

```python
JDRequirements(
    capabilities=[
        "Retrieval",
        "Ranking",
        "Production ML",
        "Evaluation"
    ]
)
```

---

# Stage 7 — JD Multi-Vector Generation

Consumes:

```python
JDRequirements
```

Builds the same 7 vector types.

---

Example

Career Vector:

```text
Candidate has shipped ranking,
retrieval and recommendation systems.
```

AI Vector:

```text
Embeddings,
Vector Databases,
LLMs,
Fine-Tuning
```

---
Now candidate vectors and JD vectors live in identical semantic spaces.

---

# Stage 8 — Multi-Index Retrieval

For each JD vector:

```python
JD Career Vector
```

searches

```python
index_career
```

---

Example

```python
career_index.search(
    jd_career_vector,
    k=5000
)
```

---

Outputs

```python
[
   (candidate_1, 0.91),
   (candidate_2, 0.89),
   ...
]
```

---

Repeat for all indexes.

---

## Candidate Pool Formation

Union all results.

Example:

```text
Career Index      → 5000
AI Index          → 5000
System Index      → 3000
Skills Index      → 3000
```

↓

```text
13,200 unique candidates
```

Only these move forward.

---

# Stage 9 — Component Similarity Computation

For every retrieved candidate:

Compute:

```python
identity_score
career_score
ai_score
system_score
skill_score
validation_score
recruitability_score
```

Example:

```python
{
    "identity": 0.84,
    "career": 0.93,
    "ai": 0.89,
    "system": 0.81
}
```

---

# Stage 10 — Semantic Aggregation

Combine all similarity scores.

```python
semantic_score =
(
0.15 * identity
+
0.30 * career
+
0.25 * ai
+
0.10 * system
+
0.10 * skill
+
0.05 * validation
+
0.05 * recruitability
)
```

Output:

```python
semantic_score = 0.886
```

---

# Stage 11 — Structured Evidence Layer

This stage consumes:

```python
CandidateEvidence
CareerIntelligence
redrob_signals
```

which were generated during preprocessing.

No re-parsing required.

---

## Experience Score

Input

```python
experience_years = 7
```

Output

```python
experience_score = 0.95
```

---

## Product Experience Score

Input

```python
career_signals=[
    "Product Company",
    "Startup"
]
```

Output

```python
product_score = 0.88
```

---

## Production ML Score

Input

```python
inferred_capabilities=[
    "Retrieval",
    "Ranking",
    "Production ML"
]
```

Output

```python
production_ml_score = 0.93
```

---

## Evaluation Score

Input

```python
evidence:
{
   "Evaluation":
   [
      "Owned NDCG benchmarks",
      "Ran A/B tests"
   ]
}
```

Output

```python
evaluation_score = 0.90
```

---

Combine:

```python
structured_score
```

---

# Stage 12 — Behavioral Layer

Consumes:

```python
redrob_signals
```

already available from preprocessing.

---

Input

```python
{
    recruiter_response_rate: 0.82,
    open_to_work: True,
    last_active: recent,
    github_activity: 78
}
```

---

Output

```python
behavior_score = 0.91
```

---

This is not a filter.

Only a multiplier.

---

# Stage 13 — Final Score

Consumes:

```python
semantic_score
structured_score
behavior_score
```

---

```python
base_score =
(
0.80 * semantic_score
+
0.20 * structured_score
)

final_score =
base_score
*
(
0.85 + 0.15*behavior_score
)
```

---

Output

```python
Candidate A = 0.903
Candidate B = 0.881
Candidate C = 0.872
```

---

# Stage 14 — Ranking

Sort:

```python
all_candidates
```

by:

```python
final_score
```

Descending.

---

# Stage 15 — Honeypot Audit (Post Layer)

Important:

This is NOT part of ranking.

The ranking system should naturally rank most honeypots low.

Only after ranking:

```python
Top 500
    ↓
Honeypot Audit
    ↓
Top 100
```

Audit checks:

```python
timeline impossibilities
career contradictions
education inconsistencies
experience mismatches
```

and removes suspicious profiles before final submission.

---

# Complete Data Flow

```text
RAW CANDIDATE
      │
      ▼
Candidate Understanding
      │
      ├── CandidateEvidence
      │
      ▼
Skill Clustering
      │
      ├── SkillClusterObject
      │
      ▼
Career Intelligence Extraction
      │
      ├── CareerIntelligence
      │
      ▼
Multi-Vector Generation
      │
      ├── Identity Vector
      ├── Career Vector
      ├── AI Vector
      ├── System Vector
      ├── Skill Vector
      ├── Validation Vector
      └── Recruitability Vector
      │
      ▼
Embeddings
      │
      ▼
7 HNSW Indexes
────────────────────────────────────────────

JD
 │
 ▼
JD Understanding
 │
 ▼
JD Multi-Vector Generation
 │
 ▼
Multi-Index Retrieval
 │
 ▼
Candidate Pool
 │
 ▼
Similarity Scoring
 │
 ▼
Semantic Aggregation
 │
 ▼
Structured Evidence Layer
 │
 ▼
Behavioral Layer
 │
 ▼
Final Score
 │
 ▼
Ranking
 │
 ▼
Honeypot Audit
 │
 ▼
Top 100
```

This version makes every artifact explicit, shows what each stage receives and emits, and ensures that nothing is recomputed unnecessarily during runtime. The runtime stage only performs JD decomposition, retrieval, scoring, and ranking; all expensive candidate understanding work is done offline.
