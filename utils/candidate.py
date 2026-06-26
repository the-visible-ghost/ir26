"""
Wrapper for Candidate JSON-Object
"""

from typing import Dict, List, Literal, Optional
import datetime as dt
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
            f"{'Currently' if self.is_current else 'Previously'} "
            f"{'an' if self.title[0] in vowels else 'a'} {self.title} "
            f"at {self.company} ({self.company_size} employees) "
            f"in {self.industry} industry for "
            f"{self.duration_months // 12} years. \n" + self.description
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
