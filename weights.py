CATEGORY_WEIGHTS = {
    "must_have": 5.0,
    "core_ml_retrieval": 4.0,
    "evaluation_ml_depth": 4.0,
    "execution_signal": 3.0,
    "nice_to_have": 1.5,
    "context": 1.0,
    "negative_signals": -4.0,
}

SECTION_WEIGHTS = {
    "skills": 1.5,
    "experience": 1.2,
    "summary": 1.0,
}

CANDIDATE_PENALTY = {
    "skills_experience_mismatch": 1,
    "summary_experience_mismatch": 0.66,
    "summary_skills_mismatch": 0.33,
}

REDROB_SIGNAL_WEIGHTS = {
    "profile_completeness_score": 0.25,
    "verified_email": 0.20,
    "verified_phone": 0.25,
    "linkedin_connected": 0.15,
    "open_to_work_flag": 0.50,
    "notice_period_days": -0.20,
    "profile_views_received_30d": 0.10,
    "search_appearance_30d": 0.10,
    "saved_by_recruiters_30d": 0.30,
    "applications_submitted_30d": 0.15,
    "recruiter_response_rate": 0.45,
    "avg_response_time_hours": -0.35,
    "github_activity_score": 0.35,
    "endorsements_received": 0.15,
    "interview_completion_rate": 0.40,
    "offer_acceptance_rate": 0.35,
    "willing_to_relocate": 0.20,
}

OVERALL_WEIGHTS = {"redrob": 0.01, "penalty": -1, "match": 1, "reranker": 1}
