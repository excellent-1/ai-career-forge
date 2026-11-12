"""Typed contracts shared by the baseline and optional model adapter."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class Requirement(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skill: str = Field(min_length=1)
    priority: Literal["required", "preferred", "unspecified"]
    evidence: str = Field(min_length=1, description="An exact, contiguous quote from the input.")


class JobAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    requirements: list[Requirement]
    unknowns: list[str]


class AnalysisRun(BaseModel):
    mode: Literal["rules", "live-ai"]
    source_sha256: str
    analysis: JobAnalysis
    warnings: list[str]
