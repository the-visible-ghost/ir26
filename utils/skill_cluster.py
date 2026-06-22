SKILL_CLUSTER_MAP = {
    "software_engineering": [
        "Python",
        "Java",
        "JavaScript",
        "TypeScript",
        "Go",
        "Rust",
        "Node.js",
        "Django",
        "Flask",
        "FastAPI",
        "Spring Boot",
        "gRPC",
        "REST APIs",
        "Microservices",
        "GraphQL",
        "Next.js",
        "React",
        "Redux",
        "Vue.js",
        "HTML",
        "CSS",
        "Tailwind",
        "Webpack",
    ],
    "data_engineering": [
        "Spark",
        "Airflow",
        "Kafka",
        "Apache Flink",
        "Apache Beam",
        "Databricks",
        "ETL",
        "Data Pipelines",
        "dbt",
        "Snowflake",
        "BigQuery",
        "Hadoop",
    ],
    "retrieval_ranking": [
        "BM25",
        "Elasticsearch",
        "OpenSearch",
        "FAISS",
        "Pinecone",
        "Weaviate",
        "Qdrant",
        "Milvus",
        "Vector Search",
        "Recommendation Systems",
        "Information Retrieval",
        "Haystack",
    ],
    "machine_learning": [
        "Feature Engineering",
        "XGBoost",
        "Statistical Modeling",
        "Forecasting",
        "scikit-learn",
        "Machine Learning",
        "Data Science",
    ],
    "deep_learning": [
        "PyTorch",
        "TensorFlow",
        "CNN",
        "GANs",
        "Object Detection",
        "Image Classification",
        "YOLO",
        "OpenCV",
        "Computer Vision",
        "Deep Learning",
        "Reinforcement Learning",
    ],
    "nlp_llm": [
        "NLP",
        "Hugging Face Transformers",
        "Fine-tuning LLMs",
        "LoRA",
        "PEFT",
        "Prompt Engineering",
        "LangChain",
        "Sentence Transformers",
        "Embeddings",
        "Speech Recognition",
        "TTS",
    ],
    "mlops": [
        "BentoML",
        "MLflow",
        "Kubeflow",
        "Weights & Biases",
        "MLOps",
        "CI/CD",
    ],
    "cloud": [
        "AWS",
        "Azure",
        "GCP",
        "Kubernetes",
        "Docker",
        "Terraform",
    ],
    "database": [
        "SQL",
        "PostgreSQL",
        "MongoDB",
        "Redis",
    ],
    "frontend": [
        "Angular",
        "Figma",
        "Illustrator",
        "Photoshop",
    ],
    "domain": [
        "Marketing",
        "Sales",
        "Salesforce CRM",
        "Accounting",
        "Tally",
        "SAP",
        "Content Writing",
        "SEO",
        "Excel",
        "PowerPoint",
    ],
    "leadership": [
        "Scrum",
        "Agile",
        "Project Management",
        "Six Sigma",
    ],
}

SKILL_TO_CLUSTER = {}
for cluster, skills in SKILL_CLUSTER_MAP.items():
    for skill in skills:
        SKILL_TO_CLUSTER[skill] = cluster


def cluster_skills(skill_names: list[str]) -> dict[str, list[str]]:
    # Map a list of skill names to cluster buckets.

    clusters = {cluster: [] for cluster in SKILL_CLUSTER_MAP}

    for skill in skill_names:
        cluster = SKILL_TO_CLUSTER.get(skill)
        if cluster:
            clusters[cluster].append(skill)

    # Return while removing empty clusterss
    return {k: v for k, v in clusters.items() if v}
