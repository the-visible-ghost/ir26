"""
Wrapper for Candidate JSON-Object
"""

# TODO: Writing from_json method for each class

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional
import datetime as dt

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


@dataclass(slots=True)
class Profile:
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


@dataclass(slots=True)
class Career:
    company: str
    title: str
    start_date: dt.date
    end_date: Optional[dt.date]
    duration_months: int
    is_currnt: bool
    industry: str
    company_size: CompanySize
    description: str


@dataclass(slots=True)
class Education:
    institution: str
    degree: str
    field_of_study: str
    start_year: int
    end_year: int
    grade: Optional[str]
    tier: EducationTier


@dataclass(slots=True)
class Skill:
    name: str
    proficiency: SkillProficiency
    endorsements: int
    duration_months: int


@dataclass(slots=True)
class Certification:
    name: str
    issuer: str
    year: int


@dataclass(slots=True)
class Language:
    language: str
    proficiency: LanguageProficiency


@dataclass(slots=True)
class RedrobSignals:
    profile_completeness_score: float
    signup_date: dt.date
    last_active_date: dt.date
    open_to_work_flag: bool
    profile_views_received_30d: int
    applications_submitted_30d: int
    recruiter_response_rate: float
    avg_response_time_hours: float
    skill_assessment_score: Dict[str, int]
    connection_count: int
    endorsements_reciever: int
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


@dataclass(slots=True)
class Candidate:
    candidate_id: str
    profile: Profile
    career_history: List[Career]
    education: List[Education]
    skills: List[Skill]
    certifications: List[Certification]
    languages: List[Language]
    redrob_signals: RedrobSignals
