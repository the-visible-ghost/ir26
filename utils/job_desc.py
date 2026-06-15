# TODO: Re-check the processed JD and further optimize/correct wherever needed.
# NOTE: Further atomize the content in some places if needed

processed = {
    "must-have": [  # Core Match / Primary Retrieval Signal
        "Senior AI Engineer role focused on production ML systems for ranking, retrieval, and candidate-job matching. ",
        "Strong experience required in embeddings-based retrieval systems deployed in production (sentence-transformers, BGE, E5, OpenAI embeddings). ",
        "Hands-on experience with vector databases or hybrid search systems such as FAISS, Milvus, Weaviate, Pinecone, Elasticsearch, or OpenSearch. ",
        "Strong Python engineering ability with production-grade code quality. ",
        "Experience designing evaluation frameworks for ranking systems including NDCG, MRR, MAP, offline-to-online evaluation, and A/B testing. ",
        "Must have built and shipped end-to-end ranking, search, recommendation, or retrieval systems to real users. ",
        "Experience must include production system ownership, embedding drift handling, index refresh strategies, and retrieval quality regression monitoring.",
    ],
    "retrieval": [  # ML System Depth / Technical Alignment Vector
        "Deep expertise in modern machine learning systems including embeddings, dense and hybrid retrieval, ranking systems, and recommendation architectures. ",
        "Experience with vector search, similarity search, and large-scale retrieval pipelines. ",
        "Understanding of tradeoffs between BM25, dense embeddings, and hybrid retrieval systems. ",
        "Knowledge of learning-to-rank approaches and ranking optimization strategies. ",
        "Experience with distributed ML inference, scalable search systems, and production ML system design. ",
        "Ability to design ranking systems that balance precision, recall, latency, and scalability.",
    ],
    "evaluation": [  # Scientific Thinking / Quality Signal Vector
        "Strong ability to design and interpret evaluation systems for ranking and retrieval. ",
        "Experience with ranking metrics such as NDCG, MRR, MAP, precision-recall tradeoffs, and ranking correlation metrics. ",
        "Ability to design offline evaluation pipelines and connect them to online A/B testing systems. ",
        "Understanding of statistical validation of ranking improvements and experiment design. ",
        "Experience building feedback loops from user behavior into ranking system improvements. ",
        "Strong intuition for measurement, experimentation, and model/system iteration.",
    ],
    "nice-to-have": [  # Expansion Vector / Optional Enrichment
        "Experience with LLM fine-tuning techniques such as LoRA, QLoRA, and PEFT. ",
        "Familiarity with retrieval-augmented generation (RAG) systems. ",
        "Experience with learning-to-rank models including XGBoost-based rankers and neural ranking models. ",
        "Exposure to HR-tech, recruiting platforms, or marketplace matching systems. ",
        "Background in distributed systems, large-scale data pipelines, or inference optimization. ",
        "Open-source contributions in machine learning or information retrieval systems.",
    ],
    "execution": [  # Product Ship Culture Vector / Behavorial Alignment
        "Ability to rapidly ship production systems with imperfect initial implementations and iterate based on real user feedback. ",
        "Comfort working in fast-paced startup environments where systems evolve rapidly. ",
        "Strong bias toward execution over research purity, with willingness to build v1 systems quickly. ",
        "Experience working closely with product and operational teams to refine ML systems in production. ",
        "Ability to work in ambiguous environments where requirements evolve continuously. ",
        "Preference for practical engineering solutions over theoretical completeness in early-stage systems.",
    ],
    "negative": [  # Disqualifiers / Rejection Criteria
        "Career experience limited to IT consulting companies such as TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini without product company ML exposure. ",
        "Pure research-only experience without production deployment of ML or ranking systems. ",
        "Recent experience limited to framework usage such as LangChain-based applications without deeper ML system ownership. ",
        "Primary background in computer vision, speech processing, or robotics without NLP or information retrieval experience. ",
        "Senior roles focused only on architecture or management without recent hands-on coding or system implementation. ",
        "Work experience entirely in closed-source proprietary environments without external validation such as open-source work, talks, or publications.",
    ],
    "context": [  # Role Reality Vector / Job Contraints + Expectations
        "Full-time Senior AI Engineer role based in Pune or Noida with hybrid work model. ",
        "Expected experience range is 5 to 9 years, with preference for 6 to 8 years in applied machine learning roles. ",
        "Role involves ownership of ranking, retrieval, and candidate-job matching systems in a talent intelligence platform. ",
        "Requires collaboration with product teams, recruiters, and engineering teams to design and iterate on ML systems. ",
        "Fast-moving startup environment with evolving requirements and ambiguous problem definitions. ",
        "Expectation of strong ownership, system thinking, and long-term commitment of 3+ years.",
    ],
}
original = """
Job Description: Senior AI Engineer
Location: Pune/Noida, India (Hybrid — flexible cadence) | Open to relocation candidates from Tier-1 Indian cities 
Employment Type: Full-time 
Experience Required: 5–9 years (see "what we mean by this" below) 

Let's be honest about this role 
If you've spent your career at Google or Meta and you want a well-scoped role with a defined ladder, this isn't it. 
If you've spent your career bouncing between early-stage startups and you want to "just code" without having to think about product or recruiter workflows or eval frameworks, this also isn't it. 
We need someone who is simultaneously comfortable with two things that sound contradictory: 
    Deep technical depth in modern ML systems — embeddings, retrieval, ranking, LLMs, fine-tuning. 
    Scrappy product-engineering attitude — willing to ship a working ranker in a week even if the underlying ML is "obviously suboptimal," because we need to learn from real users before we know what to actually optimize for. 
These are not contradictory in real life. They feel contradictory because of how engineering culture sorted itself into "researcher" vs "shipper" archetypes. We need both modes available in the same person, and we'd rather you tilt slightly toward shipper than toward researcher. 

What you'd actually be doing 
The high-level mandate: own the intelligence layer of Redrob's product. That means the ranking, retrieval, and matching systems that decide what recruiters see when they search for candidates and what candidates see when they search for roles. 
In practical terms, your first 90 days will probably look like: 
    Weeks 1-3: Audit what we currently have (it's mostly BM25 + rule-based scoring, working but not great). Identify the 3-4 highest-leverage things to fix. 
    Weeks 4-8: Ship a v2 ranking system that demonstrably improves recruiter-engagement metrics. This will involve embeddings, hybrid retrieval, and probably some LLM-based re-ranking, but the architecture is your call. 
    Weeks 9-12: Set up the evaluation infrastructure — offline benchmarks, online A/B testing, recruiter-feedback loops — so we can keep improving without flying blind. 
Beyond that, you'll be driving the long-term architecture of how we do candidate-JD matching at scale, mentoring the next round of hires (we're growing the team from 4 to 12 engineers in the next year), and working closely with our recruiter-experience PM on what to build. 

What we mean by "5-9 years" 
This is a range, not a requirement. Some people hit "senior engineer" judgment at 4 years; some never hit it after 15. We've used 5-9 because it's roughly where people we've hired into this kind of role have landed, but we'll seriously consider candidates outside the band if other signals are strong. 
That said, here are the disqualifiers we actually apply: 
    If you've spent your career in pure research environments (academic labs, research-only roles) without any production deployment — we will not move forward. We are explicit about this. We've tried it twice and it didn't work for either side. 
    If your "AI experience" consists primarily of recent (under 12 months) projects using LangChain to call OpenAI — we will probably not move forward, unless you can demonstrate substantial pre-LLM-era ML production experience. We're looking for people who understood retrieval and ranking before it became fashionable. 
    If you are a senior engineer who hasn't written production code in the last 18 months because you've moved into "architecture" or "tech lead" roles — we will probably not move forward. This role writes code. 

The skills inventory (please read carefully) 
Things you absolutely need 
    Production experience with embeddings-based retrieval systems (sentence-transformers, OpenAI embeddings, BGE, E5, or similar) deployed to real users. We don't care which model — we care that you've handled embedding drift, index refresh, retrieval-quality regression in production. 
    Production experience with vector databases or hybrid search infrastructure — Pinecone, Weaviate, Qdrant, Milvus, OpenSearch, Elasticsearch, FAISS, or something similar. Again, the specific tech doesn't matter; the operational experience does. 
    Strong Python. Yes really, we care about code quality. 
    Hands-on experience designing evaluation frameworks for ranking systems — NDCG, MRR, MAP, offline-to-online correlation, A/B test interpretation. If you've never thought about how to evaluate a ranking system rigorously, this role will be very painful. 

Things we'd like you to have but won't reject you for 
    LLM fine-tuning experience (LoRA, QLoRA, PEFT) 
    Experience with learning-to-rank models (XGBoost-based or neural) 
    Prior exposure to HR-tech, recruiting tech, or marketplace products 
    Background in distributed systems or large-scale inference optimization 
    Open-source contributions in the AI/ML space 

Things we explicitly do NOT want 
This is the section most JDs skip but we think it's the most important: 
    Title-chasers. If your career trajectory shows you optimizing for "Senior" → "Staff" → "Principal" titles by switching companies every 1.5 years, we're not a fit. We need someone who plans to be here for 3+ years. 
    Framework enthusiasts. If your GitHub is full of LangChain tutorials and your blog posts are "How I used [hot framework] to build [demo]" — that's fine but it's not what we need. We need people who think about systems, not frameworks. 
    People who have only worked at consulting firms (TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini, etc.) in their entire career. We've had bad fit experiences in both directions. If you're currently at one of these companies but have prior product-company experience, that's fine. 
    People whose primary expertise is computer vision, speech, or robotics without significant NLP/IR exposure. We respect your work but you'd be re-learning fundamentals here. 
    People whose work has been entirely on closed-source proprietary systems for 5+ years without external validation (papers, talks, open-source). We need to see how you think, not just trust that you can think. 

On location, comp, and logistics 
    Location: Pune/Noida-preferred but flexible. We have offices in Noida and Pune(mostly used Tue/Thu). We don't require any specific number of in-office days but we expect quarterly travel for offsites. Candidates in Hyderabad, Pune, Mumbai, Delhi NCR welcome to apply. Outside India: case-by-case, but we don't sponsor work visas. 
    Notice period: We'd love sub-30-day notice. We can buy out up to 30 days. 30+ day notice candidates are still in scope but the bar gets higher. 

The vibe check 
We genuinely believe culture-fit matters more at this stage than skills-fit. Skills are teachable; the rest mostly isn't. 
We work async-first and write a lot. If you find writing painful, you'll find this role painful. 
We disagree openly and decide quickly. If you find that style abrasive, you'll find this role abrasive. 
We move fast and break things, with the caveat that "things" are usually our internal assumptions, not user-facing systems. If you need a stable, mature codebase to be productive, you'll find this role unstable. 

How to read between the lines 
The "ideal candidate" we're imagining is roughly: 
    6-8 years total experience, of which 4-5 are in applied ML/AI roles at product companies (not pure services). 
    Has shipped at least one end-to-end ranking, search, or recommendation system to real users at meaningful scale. 
    Has strong opinions about retrieval (hybrid vs dense), evaluation (offline vs online), and LLM integration (when to fine-tune vs prompt) — and can defend them with reference to systems they actually built. 
    Located in or willing to relocate to Noida or Pune. 
    Active on Redrob platform (or has clear signal of being in the job market) so we can actually talk to them. 
"""
