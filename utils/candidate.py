"""
Wrapper for Candidate JSON-Object with Reason Generation
"""

from typing import Dict, List, Literal, Optional, Tuple
import datetime as dt
import numpy as np
import msgspec

from utils.skill_cluster import (
    CLUSTER_DESCRIPTIONS,
    gen_skill_cluster,
)

type CompanySize = Literal[
    "1-10",
    "11-50",
    "51-200",
    "201-500",
    "501-1000",
    "1001-5000",
    "5001-10000",
    "10001+",
]

type EducationTier = Literal["tier_1", "tier_2", "tier_3", "tier_4", "unknown"]
type SkillProficiency = Literal["beginner", "intermediate", "advanced", "expert"]
type LanguageProficiency = Literal["basic", "conversational", "professional", "native"]
type WorkMode = Literal["remote", "hybrid", "onsite", "flexible"]

type CandidateEmbedData = Dict[
    Literal["summary", "skills", "experience"], str | List[str]
]

vowels = ("a", "e", "i", "o", "u")


# Reason Feature Accumulator


class ReasonFeatures:
    def __init__(self):
        # Match quality
        self.match_score: float = 0.0
        self.match_category: str = "low"  # low, medium, high
        self.top_matching_sections: List[str] = []

        # Career analysis
        self.career_trajectory: str = "unknown"  # stable, gap, pivot, transition, fresh
        self.yoe: float = 0.0
        self.current_title: str = ""
        self.current_company: str = ""
        self.current_industry: str = ""
        self.past_titles: List[str] = []
        self.past_industries: List[str] = []
        self.has_relevant_current_role: bool = False
        self.has_relevant_past_role: bool = False

        # Skills analysis
        self.relevant_skill_count: int = 0
        self.advanced_skill_count: int = 0
        self.skill_source: str = "unknown"  # current_job, past_job, self_taught, mixed
        self.top_skills: List[str] = []
        self.skill_assessment_avg: Optional[float] = None

        # Signals
        self.profile_completeness: float = 0.0
        self.is_verified: bool = False
        self.is_active: bool = False
        self.open_to_work: bool = False
        self.response_rate: float = 0.0
        self.github_active: bool = False

        # Mismatch / penalty analysis
        self.internal_penalty: float = 0.0
        self.mismatch_type: str = (
            "none"  # none, minor, career_pivot, skill_inflation, honeypot_like
        )
        self.penalty_breakdown: Dict[str, float] = {}

        # Temporal
        self.career_gap_months: int = 0
        self.is_recent_graduate: bool = False
        self.is_career_changer: bool = False
        self.years_since_last_relevant: float = 0.0


class Profile(msgspec.Struct):
    anonymized_name: str
    headline: str
    summary: str
    location: str
    country: str
    years_of_experience: float
    current_title: str
    current_company: str
    current_company_size: CompanySize
    current_industry: str


class Career(msgspec.Struct):
    company: str
    title: str
    start_date: dt.date
    end_date: Optional[dt.date]
    duration_months: int
    is_current: bool
    industry: str
    company_size: CompanySize
    description: str

    @property
    def embed_str(self) -> str:
        return (
            f"I {'am' if self.is_current else 'was'} "
            f"{'currently' if self.is_current else 'previously'} "
            f"{'an' if self.title[0] in vowels else 'a'} {self.title} "
            f"at {self.company} ({self.company_size} employees) "
            f"in {self.industry} industry for "
            f"{self.duration_months // 12} years.\n" + self.description
        )


class Education(msgspec.Struct):
    institution: str
    degree: str
    field_of_study: str
    start_year: int
    end_year: int
    grade: Optional[str]
    tier: EducationTier


class Skill(msgspec.Struct):
    name: str
    proficiency: SkillProficiency
    endorsements: int
    duration_months: int

    @property
    def embed_str(self) -> str:
        return (
            f"{self.proficiency} proficiency in "
            f"{self.name} with "
            f"{self.duration_months // 12} years experience"
        )


class SkillCluster(msgspec.Struct):
    name: str
    desc: str
    skills: List[Skill]

    @property
    def embed_str(self) -> str:
        skills = "\n".join(" - " + skill.embed_str for skill in self.skills)
        return f"{self.name}:\n{self.desc}\n\n{skills}"


class Certification(msgspec.Struct):
    name: str
    issuer: str
    year: int


class Language(msgspec.Struct):
    language: str
    proficiency: LanguageProficiency


class RedrobSignals(msgspec.Struct):
    profile_completeness_score: float
    signup_date: dt.date
    last_active_date: dt.date
    open_to_work_flag: bool
    profile_views_received_30d: int
    applications_submitted_30d: int
    recruiter_response_rate: float
    avg_response_time_hours: float
    skill_assessment_scores: Dict[str, float]
    connection_count: int
    endorsements_received: int
    notice_period_days: int
    expected_salary_range_inr_lpa: Dict[Literal["min", "max"], float]
    preferred_work_mode: WorkMode
    willing_to_relocate: bool
    github_activity_score: float
    search_appearance_30d: int
    saved_by_recruiters_30d: int
    interview_completion_rate: float
    offer_acceptance_rate: float
    verified_email: bool
    verified_phone: bool
    linkedin_connected: bool


class Candidate(msgspec.Struct):
    candidate_id: str
    profile: Profile
    career_history: List[Career]
    education: List[Education]
    skills: List[Skill]
    certifications: List[Certification]
    languages: List[Language]
    redrob_signals: RedrobSignals

    # Mutable field for storing reason features accumulated during scoring.
    # msgspec.Struct defaults to frozen=False, so this is mutable.
    _reason_features: Optional[ReasonFeatures] = None

    @property
    def skill_clusters(self) -> Dict[str, SkillCluster]:
        return {
            name: SkillCluster(name, CLUSTER_DESCRIPTIONS[name], skills)
            for name, skills in gen_skill_cluster(self).items()
        }

    @property
    def embed_data(self) -> CandidateEmbedData:
        return {
            "summary": (
                f"I am a {self.profile.current_title}"
                f" at {self.profile.current_company}"
                f" in {self.profile.current_industry} industry."
                f" {self.profile.summary}"
            ),
            "skills": [cluster.embed_str for cluster in self.skill_clusters.values()],
            "experience": [carrer.embed_str for carrer in self.career_history],
        }

    @property
    def text(self) -> str:
        embed_data = self.embed_data
        return (
            f"Sumamary: {embed_data['summary']}. "
            f"Skills: {', '.join(skill.embed_str for skill in self.skills)}. "
            f"Experience: {', '.join(embed_data['experience'])}."
        )

    # REASON GENERATION -------------------------------------------------------------

    def _analyze_career_trajectory(self) -> Tuple[str, Dict]:
        career = self.career_history
        if not career:
            return "unknown", {}

        details = {
            "current_title": career[0].title if career else "",
            "past_titles": [c.title for c in career[1:]],
            "current_industry": career[0].industry if career else "",
            "past_industries": list(set(c.industry for c in career[1:])),
            "total_months": sum(c.duration_months for c in career),
            "gap_months": 0,
            "is_fresh": self.profile.years_of_experience < 2 and len(career) <= 2,
        }

        # Detect career gaps between consecutive jobs
        if len(career) >= 2:
            for i in range(len(career) - 1):
                current_end = career[i].end_date
                next_start = career[i + 1].start_date
                if current_end and next_start:
                    gap = (next_start - current_end).days / 30
                    if gap > 3:  # > 3 months gap
                        details["gap_months"] += int(gap)

        # Detect pivot: current role very different from past roles
        if len(career) >= 2:
            current_title_lower = career[0].title.lower()
            past_titles_lower = [c.title.lower() for c in career[1:]]

            # Simple keyword overlap for pivot detection
            current_keywords = set(current_title_lower.split())
            pivot_score = 0
            for past in past_titles_lower:
                past_keywords = set(past.split())
                overlap = len(current_keywords & past_keywords)
                union = len(current_keywords | past_keywords)
                if union > 0:
                    pivot_score += overlap / union

            avg_similarity = (
                pivot_score / len(past_titles_lower) if past_titles_lower else 1.0
            )

            if avg_similarity < 0.3 and details["gap_months"] > 6:
                return "pivot_with_gap", details
            elif avg_similarity < 0.3:
                return "pivot", details
            elif details["gap_months"] > 6:
                return "gap", details

        if details["is_fresh"]:
            return "fresh", details

        return "stable", details

    def _analyze_skill_sources(self) -> Tuple[str, List[str]]:
        career = self.career_history
        skills = self.skills

        if not skills or not career:
            return "unknown", []

        # Build text from all career entries
        all_exp_text = " ".join(f"{c.title} {c.description}".lower() for c in career)
        current_exp_text = (
            f"{career[0].title} {career[0].description}".lower() if career else ""
        )
        past_exp_text = " ".join(
            f"{c.title} {c.description}".lower() for c in career[1:]
        )

        current_matches = []
        past_matches = []
        unmatched = []

        for skill in skills:
            skill_name = skill.name.lower()
            skill_words = set(skill_name.split()) | {skill_name}

            # Check if skill appears in current role
            in_current = any(word in current_exp_text for word in skill_words)
            in_past = any(word in past_exp_text for word in skill_words)
            in_any = any(word in all_exp_text for word in skill_words)

            if in_current:
                current_matches.append(skill.name)
            elif in_past:
                past_matches.append(skill.name)
            elif in_any:
                past_matches.append(skill.name)
            else:
                unmatched.append(skill.name)

        # Determine primary source
        total = len(skills)
        current_ratio = len(current_matches) / total if total > 0 else 0
        past_ratio = len(past_matches) / total if total > 0 else 0
        unmatched_ratio = len(unmatched) / total if total > 0 else 0

        if current_ratio >= 0.6:
            return "current_job", current_matches
        elif past_ratio >= 0.5 and current_ratio < 0.3:
            return "past_job", past_matches
        elif unmatched_ratio >= 0.5:
            return "self_taught", unmatched
        else:
            return "mixed", current_matches + past_matches

    def _classify_mismatch(
        self, penalty: float, penalty_breakdown: Dict[str, float]
    ) -> str:
        if penalty < 0.2:
            return "none"

        # Check which penalties are high
        high_penalties = {k: v for k, v in penalty_breakdown.items() if v > 0.5}

        if not high_penalties:
            return "minor"

        # Career pivot: high title-exp mismatch but career is coherent
        if (
            "title_exp_penalty" in high_penalties
            and "career_penalty" not in high_penalties
        ):
            trajectory, _ = self._analyze_career_trajectory()
            if trajectory in ("pivot", "pivot_with_gap"):
                return "career_pivot"

        # Skill inflation: many advanced skills but low assessment
        if "skill_inflation_penalty" in high_penalties:
            assessments = self.redrob_signals.skill_assessment_scores
            if assessments:
                avg = np.mean(list(assessments.values()))
                if avg < 50:
                    return "honeypot_like"
            # Could be genuine expert with no assessments
            return "skill_expert"

        # Summary doesn't match experience: possible fake profile
        if (
            "summary_exp_penalty" in high_penalties
            and "skill_exp_penalty" in high_penalties
        ):
            return "honeypot_like"

        # Education issues
        if "education_penalty" in high_penalties:
            return "data_quality_issue"

        return "minor"

    def _build_reason(self, features: ReasonFeatures) -> str:
        p = self.profile
        r = self.redrob_signals
        career = self.career_history

        # Determine what makes this candidate stand out
        standout = []

        # 1. Relevant experience depth
        if features.match_score >= 0.75:
            standout.append("deep role alignment")
        elif features.match_score >= 0.5:
            standout.append("relevant background")

        # 2. Proven skills from actual work
        past_skills = [s.name for s in self.skills if s.duration_months >= 24]
        if len(past_skills) >= 2:
            standout.append(f"proven {past_skills[0]} and {past_skills[1]} expertise")
        elif len(past_skills) == 1:
            standout.append(f"proven {past_skills[0]} expertise")

        # 3. Current applicability
        if features.has_relevant_current_role:
            standout.append("actively working in a similar role")
        elif features.has_relevant_past_role and career:
            relevant_past = [c for c in career[1:] if not c.is_current]
            if relevant_past:
                standout.append(f"prior {relevant_past[0].title} experience")

        # 4. Engagement signals
        if r.open_to_work_flag and r.recruiter_response_rate > 0.5:
            standout.append("responsive and actively looking")
        elif r.open_to_work_flag:
            standout.append("open to opportunities")

        # Build the sentence
        parts = []

        # Identity clause
        identity = f"{p.years_of_experience:.0f}-year {p.current_title}"
        if career and len(career) > 1:
            past = career[1].title
            identity += f" (previously {past})"

        parts.append(identity)

        # Standout clause
        if standout:
            parts.append(f"brings {', '.join(standout)}")

        # Caveat clause (only if notable)
        caveat = ""
        trajectory, traj_details = self._analyze_career_trajectory()
        mismatch = self._classify_mismatch(
            features.internal_penalty, features.penalty_breakdown
        )

        if mismatch == "career_pivot" and traj_details.get("gap_months", 0) > 12:
            caveat = f"career gap of {traj_details['gap_months'] // 12} years"
        elif mismatch == "honeypot_like":
            caveat = "claims need verification"
        elif not (r.verified_email and r.verified_phone):
            caveat = "contact details unverified"
        elif not r.open_to_work_flag:
            caveat = "passive candidate"

        if caveat:
            parts.append(f"note: {caveat}")

        reason = ", ".join(parts) + "."
        return reason[:247] + "..." if len(reason) > 250 else reason

    @property
    def reason(self) -> str:
        if self._reason_features is not None:
            return self._build_reason(self._reason_features)

        # Fallback: basic reason without scoring context
        p = self.profile
        r = self.redrob_signals

        # Count AI-relevant skills
        ai_clusters = (
            "retrieval_ranking",
            "machine_learning",
            "nlp_llm",
            "deep_learning",
        )
        ai_skills = sum(
            len(cluster.skills)
            for name, cluster in self.skill_clusters.items()
            if name in ai_clusters
        )

        # Basic trajectory check
        trajectory, _ = self._analyze_career_trajectory()

        if trajectory == "fresh":
            return (
                f"{p.years_of_experience:.1f}YOE {p.current_title} "
                f"with {ai_skills} AI core skills; "
                f"response rate {r.recruiter_response_rate:.0%}."
            )
        elif trajectory in ("pivot", "pivot_with_gap"):
            past = (
                self.career_history[1].title
                if len(self.career_history) > 1
                else "professional"
            )
            return (
                f"Former {past} ({p.years_of_experience:.1f}YOE), "
                f"currently {p.current_title}; "
                f"{ai_skills} AI skills; "
                f"response rate {r.recruiter_response_rate:.0%}."
            )
        else:
            return (
                f"Currently {p.current_title} "
                f"with {p.years_of_experience:.1f}YOE; "
                f"{ai_skills} AI core skills; "
                f"response rate {r.recruiter_response_rate:.0%}."
            )
