from typing import List, Optional
from pydantic import BaseModel


class VerifyRequest(BaseModel):
    type: str
    input: str


class SuspiciousClaim(BaseModel):
    claim: str
    reason: str
    confidence: str


class EvidenceSource(BaseModel):
    title: str
    url: str
    snippet: str
    source: Optional[str] = ""
    credibility: Optional[str] = ""
    published_date: Optional[str] = ""


class TimelineEvent(BaseModel):
    date: str
    event: str


class SpreadingPlatform(BaseModel):
    platform: str
    spread_percentage: int


class VerifyResponse(BaseModel):
    success: bool
    trust_score: int
    verdict: str
    summary: str
    risk_level: str
    sources_checked: int
    last_verified: str
    executive_summary: Optional[str] = ""
    key_findings: List[str] = []
    suspicious_claims: List[SuspiciousClaim] = []
    triggered_indicators: List[str] = []
    evidence_sources: List[EvidenceSource] = []
    claim_timeline: List[TimelineEvent] = []
    similar_claims: List[str] = []
    spreading_on: List[SpreadingPlatform] = []
    recommendations: List[str] = []
